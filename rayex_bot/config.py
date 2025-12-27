# rayex_bot/config.py

class Messages:
    GREETING = """👋 Welcome to **Rayex**
Your trusted partner for **Naira ↔ RMB** and **USDT ↔ RMB** transactions.

Please select how I can assist you today:

**1️⃣ Exchange Naira to RMB**
**2️⃣ Exchange USDT to RMB**
**3️⃣ Rate Calculator & Check Rates**
**4️⃣ Business / Procurement Support**
**5️⃣ Speak to a Rayex Agent**"""

    ASK_CALC_AMOUNT = """🧮 **Rate Calculator**

Please enter the amount you want to convert.
(Examples: `50000 NGN`, `100 USDT`, or just `5000`)

Or reply **RATE** to just see the raw exchange rates."""

    ASK_DIRECTION = """🔁 Which transaction would you like to make?

• Naira ➝ RMB
• USDT ➝ RMB"""

    ASK_DESTINATION = """📍 Where should the RMB be sent?

• Bank Account
• WeChat Pay
• Alipay"""

    ASK_AMOUNT = """💰 Please enter the **exact amount** you want to exchange
(Example: 250,000 NGN or 18,000 USDT)"""

    ASK_DETAILS_BANK = """Please provide the recipient details:
1. Full Name (as on account)
2. Bank Name
3. Account Number"""

    ASK_DETAILS_ALIPAY_WECHAT = """Please provide the recipient details:
1. Registered Full Name
2. QR Code (You can describe it here for now example: "QR Image Sent")
3. Account region (Mainland China / Foreign)"""

    ASK_PURPOSE = """📝 What is the purpose of this payment?
(Examples: goods purchase, tuition, logistics, personal transfer)"""

    ASK_USDT_NETWORK = """⚠️ Please confirm:
• Network used
• Sender wallet is yours

Incorrect networks may lead to permanent loss.
Enter Network (TRC20 / ERC20):"""

    PROCUREMENT_INIT = """🏭 Please share:
• Product name
• Quantity
• Target price (if any)
• Supplier location (if known)
• Do you need payment + sourcing or payment only?"""

    HANDOFF = """⚠️ This transaction requires additional verification.
A Rayex agent will assist you shortly."""

    CLOSING = """Thank you for choosing **Rayex**.
Trusted • Reliable • Secure."""

    INVALID_INPUT = "❌ Invalid input. Please try again."

    @staticmethod
    def get_summary(txn_type, amount, method, estimated_rmb, rate_type):
        return f"""✅ **Transaction Summary**

• Type: {txn_type}
• Amount Sent: {amount}
• Delivery Method: {method}
• Estimated RMB Received: ¥{estimated_rmb}
• Rate Type: {rate_type}

⚠️ Rates are time-sensitive and valid for a limited window.

Reply **CONFIRM** to proceed or **EDIT** to change details."""

class Rates:
    # NGN -> RMB (e.g. 230 Naira = 1 RMB)
    NGN_TO_RMB_RATE = 215
    
    # USDT -> RMB (e.g. 1 USDT = 7.20 RMB)
    USDT_TO_RMB_RATE = 6.70
    
    @staticmethod
    def calculate_rmb_from_ngn(ngn_amount: float) -> float:
        """
        Convert Naira to RMB.
        Formula: RMB = Naira / Rate
        """
        if Rates.NGN_TO_RMB_RATE <= 0: return 0.0
        return ngn_amount / Rates.NGN_TO_RMB_RATE
        
    @staticmethod
    def calculate_rmb_from_usdt(usdt_amount: float) -> float:
        """
        Convert USDT to RMB.
        Formula: RMB = USDT * Rate
        """
        return usdt_amount * Rates.USDT_TO_RMB_RATE
