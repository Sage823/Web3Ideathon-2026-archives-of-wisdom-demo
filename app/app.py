from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from flask import Flask, flash, redirect, render_template, request, session, url_for


@dataclass(frozen=True)
class Course:
    id: int
    title: str
    creator: str
    price_eth: float
    price_usd: int
    category: str
    students: int
    rating: float


@dataclass(frozen=True)
class Badge:
    name: str
    description: str


COURSES: List[Course] = [
    Course(
        id=1,
        title="DeFi Fundamentals",
        creator="0x3f...2Bc",
        price_eth=0.08,
        price_usd=160,
        category="DeFi",
        students=234,
        rating=4.8,
    ),
    Course(
        id=2,
        title="Blockchain Basics",
        creator="0x91...aE1",
        price_eth=0.05,
        price_usd=100,
        category="Foundations",
        students=512,
        rating=4.6,
    ),
    Course(
        id=3,
        title="Web3 Investing",
        creator="0xB2...9cD",
        price_eth=0.12,
        price_usd=240,
        category="Investing",
        students=189,
        rating=4.7,
    ),
    Course(
        id=4,
        title="Smart Contract Security",
        creator="0x8a...F10",
        price_eth=0.10,
        price_usd=200,
        category="Security",
        students=143,
        rating=4.9,
    ),
]

BADGES: List[Badge] = [
    Badge(name="DeFi Scholar", description="Completed 3 DeFi courses"),
    Badge(name="Early Adopter", description="Joined in first month"),
    Badge(name="Quiz Master", description="Perfect score on quiz"),
]


def course_by_id(course_id: int) -> Optional[Course]:
    for c in COURSES:
        if c.id == course_id:
            return c
    return None


def _init_session() -> None:
    session.setdefault("wallet_connected", False)
    session.setdefault("wallet_address", None)
    session.setdefault("owned_course_ids", [])
    session.setdefault("completed_course_ids", [])
    session.setdefault("certificates", [])  # list[dict]
    session.setdefault("badges", [])  # list[dict]
    session.setdefault("listings", {})  # dict[id] = "listed"

    # Give everyone a starter badge for the dashboard vibe
    if not session["badges"]:
        session["badges"] = [{"name": "Early Adopter", "description": "Joined in first month"}]


def _wallet_short(addr: Optional[str]) -> str:
    if not addr:
        return ""
    if len(addr) <= 10:
        return addr
    return f"{addr[:4]}...{addr[-4:]}"


def _course_certificate(course: Course) -> Dict[str, Any]:
    return {
        "course_id": course.id,
        "course_title": course.title,
        "issued_to": session.get("wallet_address") or "0x7f...3dE2",
        "soulbound": True,
    }


def _ensure_unique_append(list_key: str, item: Dict[str, Any], unique_field: str) -> None:
    items = list(session.get(list_key, []))
    if any(x.get(unique_field) == item.get(unique_field) for x in items):
        session[list_key] = items
        return
    items.append(item)
    session[list_key] = items


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = "aow-demo-dev-secret"  # demo-only; replace for production

    @app.before_request
    def ensure_session_state() -> None:
        _init_session()

    @app.context_processor
    def inject_globals() -> Dict[str, Any]:
        return {
            "wallet_connected": bool(session.get("wallet_connected")),
            "wallet_address": session.get("wallet_address"),
            "wallet_short": _wallet_short(session.get("wallet_address")),
        }

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/courses")
    def courses():
        owned_ids = set(session.get("owned_course_ids", []))
        completed_ids = set(session.get("completed_course_ids", []))
        listings = session.get("listings", {}) or {}
        return render_template(
            "courses.html",
            courses=COURSES,
            owned_ids=owned_ids,
            completed_ids=completed_ids,
            listings=listings,
        )

    @app.get("/dashboard")
    def dashboard():
        owned_ids = set(session.get("owned_course_ids", []))
        owned_courses = [c for c in COURSES if c.id in owned_ids]
        listings = session.get("listings", {}) or {}
        return render_template(
            "dashboard.html",
            owned_courses=owned_courses,
            certificates=session.get("certificates", []),
            badges=session.get("badges", []),
            listings=listings,
        )

    @app.get("/course/<int:course_id>")
    def course_detail(course_id: int):
        course = course_by_id(course_id)
        if not course:
            flash("Course not found.", "danger")
            return redirect(url_for("courses"))

        owned_ids = set(session.get("owned_course_ids", []))
        completed_ids = set(session.get("completed_course_ids", []))
        has_certificate = any(
            c.get("course_id") == course_id for c in (session.get("certificates") or [])
        )
        return render_template(
            "course_detail.html",
            course=course,
            owned=(course_id in owned_ids),
            completed=(course_id in completed_ids),
            has_certificate=has_certificate,
            related_badges=BADGES,
        )

    @app.post("/connect_wallet")
    def connect_wallet():
        session["wallet_connected"] = True
        session["wallet_address"] = "0x7f12cA90bB33dE2a44F0cE11D9aC3a2b7A9b3dE2"
        flash("Wallet connected: 0x7f...3dE2", "success")
        return redirect(request.referrer or url_for("index"))

    @app.post("/buy/<int:course_id>")
    def buy(course_id: int):
        course = course_by_id(course_id)
        if not course:
            flash("Course not found.", "danger")
            return redirect(url_for("courses"))

        owned = list(session.get("owned_course_ids", []))
        if course_id in owned:
            flash("You already own this Course NFT.", "info")
            return redirect(request.referrer or url_for("courses"))

        owned.append(course_id)
        session["owned_course_ids"] = owned
        flash("Success! NFT added to wallet.", "success")
        return redirect(request.referrer or url_for("dashboard"))

    @app.post("/complete/<int:course_id>")
    def complete(course_id: int):
        course = course_by_id(course_id)
        if not course:
            flash("Course not found.", "danger")
            return redirect(url_for("courses"))

        owned = set(session.get("owned_course_ids", []))
        if course_id not in owned:
            flash("You need to own the Course NFT to complete it.", "warning")
            return redirect(url_for("course_detail", course_id=course_id))

        completed = list(session.get("completed_course_ids", []))
        if course_id not in completed:
            completed.append(course_id)
            session["completed_course_ids"] = completed

        _ensure_unique_append("certificates", _course_certificate(course), unique_field="course_id")

        # Simple badge rule for the demo: completing any course grants "Quiz Master"
        _ensure_unique_append(
            "badges",
            {"name": "Quiz Master", "description": "Perfect score on quiz"},
            unique_field="name",
        )

        flash("Certificate Minted! (Soulbound)", "success")
        flash("New badge earned: Quiz Master", "info")
        return redirect(url_for("course_detail", course_id=course_id))

    @app.post("/resell/<int:course_id>")
    def resell(course_id: int):
        owned = set(session.get("owned_course_ids", []))
        if course_id not in owned:
            flash("You don't own this Course NFT.", "warning")
            return redirect(request.referrer or url_for("dashboard"))

        listings = dict(session.get("listings", {}) or {})
        listings[str(course_id)] = "listed"
        session["listings"] = listings
        flash("Listed for sale.", "success")
        return redirect(request.referrer or url_for("dashboard"))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

