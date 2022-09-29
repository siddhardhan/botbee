from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt, ConfirmPrompt
from botbuilder.core import MessageFactory
from botbuilder.schema import InputHints


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

        
        msg_text = "your order details : " + str(step_context.result)
        msg = MessageFactory.text(
                    msg_text, msg_text, InputHints.ignoring_input
                )
        await step_context.context.send_activity(msg)
        user_details = step_context.options

        return await step_context.end_dialog(user_details)