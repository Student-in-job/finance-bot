import pandas as pd
from io import BytesIO, StringIO
from sqlalchemy import extract
from telegram import Update
from telegram.ext import ContextTypes
from database import SessionLocal, Expense, Category
from ai_engine import parse_spending
from security import is_user_admin, register_admin

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.channel_post or update.message
    if not msg or not msg.text: return

    with SessionLocal() as session:
        cats = session.query(Category).all()
        if not cats: return
            
        cat_context = "\n".join([f"- {c.name} (tags: {c.tags})" for c in cats])
        
        try:
            data = parse_spending(msg.text, cat_context)
            target_cat = session.query(Category).filter_by(name=data['category']).first()
            
            new_expense = Expense(
                message_date=msg.date,
                amount=data['amount'],
                currency=data['currency'],
                raw_text=msg.text,
                category_id=target_cat.id if target_cat else None
            )
            session.add(new_expense)
            session.commit()
        except Exception as e:
            print(f"Error: {e}")

async def auth_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pin = context.args[0] if context.args else ""
    success = register_admin(update.effective_user.id, update.effective_user.username, pin)
    text = "✅ Admin Registered!" if success else "❌ Invalid PIN."
    await update.message.reply_text(text)

async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_user_admin(update.effective_user.id):
        await update.message.reply_text("🔒 Admin access required.")
        return
        
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /report MM YYYY")
        return

    month, year = int(context.args[0]), int(context.args[1])
    
    with SessionLocal() as session:
        query = session.query(
            Expense.message_date, 
            Category.name.label('category_name'), 
            Expense.amount
        ).join(Category).filter(
            extract('month', Expense.message_date) == month,
            extract('year', Expense.message_date) == year
        )
        
        df = pd.read_sql(query.statement, session.bind)
        if df.empty:
            await update.message.reply_text("No data.")
            return

        summary = df.groupby('category_name')['amount'].sum().to_dict()
        max_val = max(summary.values())
        total_val = sum(summary.values())
        
        report_text = f"📊 **Report {month}/{year}**\n\n"
        for cat, amt in sorted(summary.items(), key=lambda x: x[1], reverse=True):
            bar = "▇" * int((amt/max_val)*10)
            report_text += f"**{cat}**\n`{bar}` {amt}\n"
        report_text += f"\n💰 **Total: {total_val}**"
        
        await update.message.reply_text(report_text, parse_mode="Markdown")

async def list_cats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_user_admin(update.effective_user.id):
        await update.message.reply_text("🔒 Admin access required.")
        return

    with SessionLocal() as session:
        cats = session.query(Category).all()
        if not cats:
            await update.message.reply_text("No categories found.")
            return

        msg = "📋 **Available Categories:**\n\n"
        for c in cats:
            msg += f"🔹 **{c.name}** (tags: `{c.tags}`)\n"
        
        await update.message.reply_text(msg, parse_mode="Markdown")

async def new_cat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_user_admin(update.effective_user.id):
        await update.message.reply_text("🔒 Admin access required.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /new_cat <NAME> <TAG1,TAG2,TAG3>")
        return

    parts = " ".join(context.args).split(",")
    name = parts[0].strip().title()
    tags = [t.strip().lower() for t in parts[1:] if t.strip()]

    if not name:
        await update.message.reply_text("❌ Invalid name.")
        return

    with SessionLocal() as session:
        cat = Category(name=name, tags=tags)
        session.add(cat)
        session.commit()
    
    await update.message.reply_text(f"✅ Category **{name}** created with tags: {', '.join(tags)}", parse_mode="Markdown")

async def delete_cat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_user_admin(update.effective_user.id):
        await update.message.reply_text("🔒 Admin access required.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /delete_cat <Category Name>")
        return

    name = context.args[0].strip().title()

    with SessionLocal() as session:
        cat = session.query(Category).filter_by(name=name).first()
        if not cat:
            await update.message.reply_text(f"❌ Category **{name}** not found.", parse_mode="Markdown")
            return
        session.delete(cat)
        session.commit()
    
    await update.message.reply_text(f"🗑️ Category **{name}** deleted.", parse_mode="Markdown")  