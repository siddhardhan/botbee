from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt, ConfirmPrompt
from botbuilder.core import MessageFactory
from botbuilder.schema import InputHints

import pandas as pd
import string
import random
import orderApp
from datetime import date


class CreateOrderDialog(ComponentDialog):
    def __init__(self, dialog_id:str = None):
        super(CreateOrderDialog, self).__init__(dialog_id or CreateOrderDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [self.order_step, self.summary_step]
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def order_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        message_text = "Please provide the order details."
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input)
        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

    
    
    async def summary_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        user_details = step_context.options
        user_id = user_details.user_id
        order_desc = str(step_context.result)
        #generate order id
        N = 4
        order_id = ''.join(random.choices(string.digits, k= N))
        order_id = 'ord' + order_id
        order_date =date.today()
        order_status = "Order Received"

        df = pd.DataFrame()
        items = []
        items.append(order_desc)
        df['order_description'] = items
        df['user_id'] = user_id
        df['order_id'] = order_id
        df['order_status'] = order_status
        df['creation_date'] = order_date
        

        print(df)
        orderApp.addOrders(df)

        msg_text = ("Your order number is " + order_id + ".")

        msg = MessageFactory.text(
            msg_text, msg_text, InputHints.ignoring_input
        )
        await step_context.context.send_activity(msg)
        
        return await step_context.end_dialog(user_details)