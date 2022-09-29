from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt, ConfirmPrompt
from botbuilder.core import MessageFactory, TurnContext, CardFactory, UserState
from botbuilder.schema import InputHints, CardAction, ActionTypes, SuggestedActions


class ViewOrderDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(ViewOrderDialog, self).__init__(dialog_id or ViewOrderDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__, []
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__