from uuid import uuid4

from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app.core.config import DATA_PATH
from app.extensions import db
from app.models import ChatMessage, ChatSession, Document
from app.rag.ingest import ingest_documents
from app.rag.qa_chain import build_qa_chain

main_bp = Blueprint("main", __name__)


def _get_or_create_session(user_id, session_id, first_message):
    session = None
    if session_id:
        session = ChatSession.query.filter_by(id=session_id, user_id=user_id).first()

    if session is None:
        title = first_message[:50] + ("..." if len(first_message) > 50 else "")
        session = ChatSession(user_id=user_id, title=title)
        db.session.add(session)
        db.session.commit()

    return session


@main_bp.route("/")
@login_required
def index():
    return render_template("index.html")


@main_bp.route("/ask", methods=["POST"])
@login_required
def ask():
    data = request.get_json(silent=True) or {}
    query = (data.get("query") or "").strip()
    session_id = data.get("session_id")

    if not query:
        return jsonify({"error": "No query provided"}), 400

    chain = build_qa_chain(current_user.id)
    if chain is None:
        return jsonify({"error": "No documents uploaded yet. Upload a PDF first."}), 400

    try:
        answer = chain.invoke(query)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    session = _get_or_create_session(current_user.id, session_id, query)
    db.session.add(ChatMessage(session_id=session.id, role="user", content=query))
    db.session.add(ChatMessage(session_id=session.id, role="assistant", content=answer))
    db.session.commit()

    return jsonify({"answer": answer, "session_id": session.id})


@main_bp.route("/api/sessions", methods=["GET"])
@login_required
def list_sessions():
    sessions = (
        ChatSession.query.filter_by(user_id=current_user.id)
        .order_by(ChatSession.created_at.desc())
        .all()
    )
    return jsonify(
        [{"id": s.id, "title": s.title, "created_at": s.created_at.isoformat()} for s in sessions]
    )


@main_bp.route("/api/sessions", methods=["POST"])
@login_required
def create_session():
    session = ChatSession(user_id=current_user.id, title="New Chat")
    db.session.add(session)
    db.session.commit()
    return jsonify({"id": session.id, "title": session.title}), 201


@main_bp.route("/api/sessions/<int:session_id>/messages", methods=["GET"])
@login_required
def get_session_messages(session_id):
    session = ChatSession.query.filter_by(id=session_id, user_id=current_user.id).first()
    if session is None:
        return jsonify({"error": "Not found"}), 404

    return jsonify([{"role": m.role, "content": m.content} for m in session.messages])


@main_bp.route("/api/documents", methods=["GET"])
@login_required
def list_documents():
    docs = (
        Document.query.filter_by(user_id=current_user.id)
        .order_by(Document.upload_date.desc())
        .all()
    )
    return jsonify(
        [
            {
                "id": d.id,
                "original_filename": d.original_filename,
                "status": d.status,
                "upload_date": d.upload_date.isoformat(),
            }
            for d in docs
        ]
    )


@main_bp.route("/api/documents", methods=["POST"])
@login_required
def upload_document():
    file = request.files.get("file")
    if not file or not file.filename:
        return jsonify({"error": "No file provided"}), 400
    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    stored_name = f"{uuid4().hex}.pdf"
    user_dir = DATA_PATH / f"user_{current_user.id}"
    user_dir.mkdir(parents=True, exist_ok=True)
    file.save(str(user_dir / stored_name))

    doc = Document(
        user_id=current_user.id,
        stored_filename=stored_name,
        original_filename=secure_filename(file.filename),
        status="pending",
    )
    db.session.add(doc)
    db.session.commit()

    try:
        ingest_documents(current_user.id)
        doc.status = "indexed"
    except Exception:
        doc.status = "failed"
    db.session.commit()

    return (
        jsonify({"id": doc.id, "original_filename": doc.original_filename, "status": doc.status}),
        201,
    )


@main_bp.route("/api/documents/<int:doc_id>", methods=["DELETE"])
@login_required
def delete_document(doc_id):
    doc = Document.query.filter_by(id=doc_id, user_id=current_user.id).first()
    if doc is None:
        return jsonify({"error": "Not found"}), 404

    user_dir = DATA_PATH / f"user_{current_user.id}"
    file_path = user_dir / doc.stored_filename
    if file_path.exists():
        file_path.unlink()

    db.session.delete(doc)
    db.session.commit()

    ingest_documents(current_user.id)

    return jsonify({"status": "deleted"})
