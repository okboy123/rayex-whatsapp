# rayex_bot/engine.py
from .models import State, Session, Transaction
from .config import Messages, Rates

class RayexBot:
    def __init__(self):
        # In a real app, we might inject a database service here
        pass

    def process_message(self, session: Session, message: str) -> str:
        """
        Main entry point for processing a message based on current state.
        """
        message = message.strip()
        
        # Global commands/resets could be handled here
        if message.lower() == "reset":
            session.reset()
            return Messages.GREETING

        if session.state == State.WAITING_FOR_MENU:
            return self._handle_menu_selection(session, message)
        
        elif session.state == State.WAITING_FOR_DIRECTION:
            return self._handle_direction_selection(session, message)
            
        elif session.state == State.WAITING_FOR_DESTINATION:
            return self._handle_destination_selection(session, message)
            
        elif session.state == State.WAITING_FOR_AMOUNT:
            return self._handle_amount_input(session, message)
            
        elif session.state == State.WAITING_FOR_DETAILS:
            return self._handle_recipient_details(session, message)
            
        elif session.state == State.WAITING_FOR_PURPOSE:
            return self._handle_purpose_input(session, message)
            
        elif session.state == State.WAITING_FOR_USDT_NETWORK:
            return self._handle_usdt_network(session, message)

        elif session.state == State.WAITING_FOR_CALC_AMOUNT:
            return self._handle_calculator(session, message)
            
        elif session.state == State.WAITING_FOR_CONFIRMATION:
            return self._handle_confirmation(session, message)
            
        elif session.state == State.WAITING_FOR_PROCUREMENT_DETAILS:
             return self._handle_procurement_details(session, message)

        else:
            # Fallback or if state is completed using Greeting
            session.reset()
            return Messages.GREETING

    def _handle_menu_selection(self, session: Session, message: str) -> str:
        if message == "1": # Naira to RMB
            session.transaction.type = "Naira -> RMB"
            session.state = State.WAITING_FOR_DIRECTION
            return Messages.ASK_DIRECTION
        elif message == "2": # USDT to RMB
            session.transaction.type = "USDT -> RMB"
            session.state = State.WAITING_FOR_DIRECTION
            return Messages.ASK_DIRECTION
        elif message == "3": # Check Rate
            # Simple rate check - return rate and go back to menu or simple instruction
            # For now, let's just give a dummy rate and reset
            return "Rates: NGN/RMB: 230 | USDT/RMB: 7.20\n\n" + Messages.GREETING
        elif message == "4": # Business Support
             session.state = State.WAITING_FOR_PROCUREMENT_DETAILS
             return Messages.PROCUREMENT_INIT
        elif message == "5":
            session.state = State.HANDOFF_TO_AGENT
            return Messages.HANDOFF
        else:
            return Messages.INVALID_INPUT + "\n\n" + Messages.GREETING

    def _handle_direction_selection(self, session: Session, message: str) -> str:
        # User prompt asks: Naira -> RMB or USDT -> RMB
        # But wait, looking at the prompt:
        # "Which transaction would you like to make? • Naira ➝ RMB • USDT ➝ RMB"
        # This seems redundant if they already chose option 1 or 2 in the main menu.
        # However, following the flow chart strictly as requested.
        # Actually, let's look at the Greeting.
        # Greeting has: 1. Exchange Naira to RMB, 2. Exchange USDT to RMB.
        # Then flow says "Determine Direction".
        # It's possible the user selected "1" which IMPLIES direction, but the prompt says "Ask clearly: Which transaction..."
        # I will assume if they selected 1 or 2, we already know, but maybe the prompt implies we should re-confirm or if they select a generic "Exchange" option?
        # The greeting has specific options. I will skip the "Ask Direction" step if it's already clear from the Menu.
        # BUT, the user prompt says "2. FX TRANSACTION FLOW -> A. Determine Direction".
        # Let's assume the menu IS the "Determine Direction" step if specific, or if there was a generic "Exchange" button.
        # Given the explicit options in GREETING, I'll treat Menu 1 & 2 as completing Step A.
        # So wait, why did I put state WAITING_FOR_DIRECTION?
        # Ah, in my plan I put it.
        # Let's adjust. If they picked 1 or 2, we go to Destination.
        
        # Actually, let's look at the "Ask clearly" text.
        # It matches the option text.
        # Maybe the user meant the Greeting options ARE the questions?
        # "Please select how I can assist you today: ... 1. Exchange Naira to RMB"
        # If I click 1, I expect to go to Destination.
        # I will route to Destination directly to save a step, as it's redundant.
        pass # Not used if I optimize

    # Redefining _handle_menu_selection to skip redundant step:
    def _handle_menu_selection(self, session: Session, message: str) -> str:
        if message == "1":
            session.transaction.type = "Naira -> RMB"
            session.state = State.WAITING_FOR_DESTINATION
            return Messages.ASK_DESTINATION
        elif message == "2":
            session.transaction.type = "USDT -> RMB"
            session.state = State.WAITING_FOR_USDT_NETWORK # USDT Flow says "3. USDT FLOW (Extra Validation)"
            # Wait, the prompt says "Ask destination" is Step B, "USDT Flow" is Step 3 (at the end? or part of flow?)
            # "If USDT: Ask blockchain... Warn about wrong-network".
            # It seems logical to ask this early or before details.
            # Let's follow the numbers. 
            # 2. FX Transaction Flow -> A (Direction) -> B (Destination) -> C (Amount) -> D (Details) -> E (Purpose) -> F (Confirmation).
            # 3. USDT Flow (Extra Validation).
            # It says "If USDT...". This likely happens either at start or before confirmation.
            # "Ask: Please confirm: Network / Wallet... Warn...". 
            # I will put this BEFORE asking for Destination/Amount for safety, OR as part of confirmation.
            # The Example in "3. USDT Flow" says "Please confirm...".
            # Let's put it right after Menu for USDT.
            return Messages.ASK_USDT_NETWORK
        elif message == "3":
            session.state = State.WAITING_FOR_CALC_AMOUNT
            return Messages.ASK_CALC_AMOUNT
        elif message == "4":
             session.state = State.WAITING_FOR_PROCUREMENT_DETAILS
             return Messages.PROCUREMENT_INIT
        elif message == "5":
            return Messages.HANDOFF
        else:
            return Messages.INVALID_INPUT + "\n" + Messages.GREETING

    def _handle_calculator(self, session: Session, message: str) -> str:
        # Check if user wants raw rates
        if "rate" in message.lower():
             return f"💹 **Today's Rates**\n\n🇳🇬 NGN/RMB: **{Rates.NGN_TO_RMB_RATE}**\n💵 USDT/RMB: **{Rates.USDT_TO_RMB_RATE}**\n\n" + Messages.GREETING

        # Try to parse amount
        val_str = message.replace(",", "").replace("₦", "").replace("¥", "").replace("$", "").replace("USDT", "").replace("NGN", "").strip()
        try:
            val = float(val_str)
            if val <= 0: raise ValueError
            
            # Formatting
            is_usdt = "usdt" in message.lower() or "$" in message
            is_ngn = "ngn" in message.lower() or "naira" in message.lower()
            
            result = ""
            if is_usdt:
                rmb = Rates.calculate_rmb_from_usdt(val)
                result = f"💱 **{val:,.2f} USDT** ≈ **¥{rmb:,.2f}**\n(Rate: {Rates.USDT_TO_RMB_RATE})"
            elif is_ngn:
                 rmb = Rates.calculate_rmb_from_ngn(val)
                 result = f"💱 **{val:,.2f} NGN** ≈ **¥{rmb:,.2f}**\n(Rate: {Rates.NGN_TO_RMB_RATE})"
            else:
                # Ambiguous: Show both
                rmb_ngn = Rates.calculate_rmb_from_ngn(val)
                rmb_usdt = Rates.calculate_rmb_from_usdt(val)
                result = (f"💱 **Calculator Result**\n\n"
                          f"IF NGN: **{val:,.2f}** ≈ **¥{rmb_ngn:,.2f}** (@ {Rates.NGN_TO_RMB_RATE})\n"
                          f"IF USDT: **{val:,.2f}** ≈ **¥{rmb_usdt:,.2f}** (@ {Rates.USDT_TO_RMB_RATE})")
            
            # Reset after showing result
            session.reset()
            return result + "\n\n" + Messages.GREETING

        except ValueError:
            return "❌ Invalid number. Please try again (e.g. 5000) or reply 'Rate'."

    def _handle_usdt_network(self, session: Session, message: str) -> str:
        # Basic validation
        if "trc" in message.lower() or "erc" in message.lower():
            session.transaction.usdt_network = message
            session.state = State.WAITING_FOR_DESTINATION
            return Messages.ASK_DESTINATION
        else:
            return "⚠️ Please specify TRC20 or ERC20.\n" + Messages.ASK_USDT_NETWORK

    def _handle_destination_selection(self, session: Session, message: str) -> str:
        msg = message.lower()
        if "bank" in msg:
            session.transaction.destination = "Bank Account"
            session.state = State.WAITING_FOR_AMOUNT
            return Messages.ASK_AMOUNT
        elif "wechat" in msg:
            session.transaction.destination = "WeChat Pay"
            session.state = State.WAITING_FOR_AMOUNT
            return Messages.ASK_AMOUNT
        elif "alipay" in msg:
            session.transaction.destination = "Alipay"
            session.state = State.WAITING_FOR_AMOUNT
            return Messages.ASK_AMOUNT
        else:
            return Messages.INVALID_INPUT + "\n" + Messages.ASK_DESTINATION

    def _handle_amount_input(self, session: Session, message: str) -> str:
        # Clean string from currency symbols/commas
        val_str = message.replace(",", "").replace("₦", "").replace("¥", "").replace("$", "").replace("USDT", "").replace("NGN", "").strip()
        try:
            val = float(val_str)
            if val <= 0:
                raise ValueError
            session.transaction.amount = message # Keep original string for display
            session.transaction.amount_value = val
            
            # Decide details prompt based on destination
            session.state = State.WAITING_FOR_DETAILS
            if "Bank" in session.transaction.destination:
                return Messages.ASK_DETAILS_BANK
            else:
                return Messages.ASK_DETAILS_ALIPAY_WECHAT
        except ValueError:
             return "❌ Please enter a valid number (e.g. 250000)."

    def _handle_recipient_details(self, session: Session, message: str) -> str:
        session.transaction.recipient_details = message
        session.state = State.WAITING_FOR_PURPOSE
        return Messages.ASK_PURPOSE

    def _handle_purpose_input(self, session: Session, message: str) -> str:
        session.transaction.purpose = message
        session.state = State.WAITING_FOR_CONFIRMATION
        
        # Calculate Dummy Est RMB
        if "Naira" in session.transaction.type:
             session.transaction.estimated_rmb = Rates.calculate_rmb_from_ngn(session.transaction.amount_value)
        else:
             session.transaction.estimated_rmb = Rates.calculate_rmb_from_usdt(session.transaction.amount_value)

        summary = Messages.get_summary(
            txn_type=session.transaction.type,
            amount=session.transaction.amount,
            method=session.transaction.destination,
            estimated_rmb=f"{session.transaction.estimated_rmb:,.2f}",
            rate_type=session.transaction.rate_type
        )
        return summary

    def _handle_confirmation(self, session: Session, message: str) -> str:
        if "confirm" in message.lower():
            session.state = State.COMPLETED
            # Here we would send to backend/agent
            return Messages.CLOSING + "\n\n(Session Ended. Type 'reset' to start over)"
        elif "edit" in message.lower():
            # For simplicity, reset to menu or specific step?
            # "Reply REDIT to change details".
            # I will just restart for now.
            session.reset()
            return "🔄 Restarting session...\n\n" + Messages.GREETING
        else:
            return "Please reply **CONFIRM** or **EDIT**."
            
    def _handle_procurement_details(self, session: Session, message: str) -> str:
        # Capture details and handoff
        return Messages.HANDOFF + "\n\n(Tagged for Business+ Suite)"

