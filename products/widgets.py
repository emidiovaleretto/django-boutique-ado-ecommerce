from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _


class CustomClearableFileInput(ClearableFileInput):
    clear_checkbox_label = _("Clear")
    initial_text = _("Currently")
    input_text = _("Change")
    template_name = "products/custom_widget_templates/custom_clearable_file_input.html"
