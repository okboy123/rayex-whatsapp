# rayex_bot/models.py
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Optional

class State(Enum):
    WAITING_FOR_MENU = auto()
    # FX Flow
    WAITING_FOR_DIRECTION = auto()
    WAITING_FOR_DESTINATION = auto()
    WAITING_FOR_AMOUNT = auto()
    WAITING_FOR_DETAILS = auto()
    WAITING_FOR_PURPOSE = auto()
    WAITING_FOR_CONFIRMATION = auto()
    
    # USDT Specific
    WAITING_FOR_USDT_NETWORK = auto()
    WAITING_FOR_CALC_AMOUNT = auto()
    
    # Business Flow
    WAITING_FOR_PROCUREMENT_DETAILS = auto()
    
    # Agent Handoff
    HANDOFF_TO_AGENT = auto()
    
    # Completed
    COMPLETED = auto()

@dataclass
class Transaction:
    type: str = "" # Naira->RMB or USDT->RMB
    direction_menu_choice: str = "" 
    destination: str = "" # Bank, WeChat, Alipay
    amount: str = ""
    amount_value: float = 0.0
    currency: str = ""
    recipient_details: str = ""
    purpose: str = ""
    usdt_network: str = ""
    estimated_rmb: float = 0.0
    rate_type: str = "Standard" # Default for now

@dataclass
class Session:
    user_id: str
    state: State = State.WAITING_FOR_MENU
    transaction: Transaction = field(default_factory=Transaction)
    last_message: str = ""

    def reset(self):
        self.state = State.WAITING_FOR_MENU
        self.transaction = Transaction()
