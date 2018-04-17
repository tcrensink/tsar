#%%
import urwid
import config_files.default_config as params
from datetime import datetime
# import time

class SelectScreen(urwid.WidgetWrap):
    """
    arguments:  screen_state = {display, edit}
    record_dict: fields are names of schema fields (str) and values are objects type(index.schema[field])
    """
    def __init__(self, screen_state='display'):

        self._screen_state = screen_state
        self.field_label_widgets = [urwid.AttrMap(urwid.SelectableIcon(field_name), 'unselected_attr', focus_map='unselected_attr') for field_name in params.FIELD_NAMES]
        # self.field_data_widgets = {}
        self.modified_record_dict = None

        self.title = [urwid.Text(('prompt_attr', '(Name of record)'))]
        self.header = urwid.Pile(self.title + self.field_label_widgets)

        self.modified_record_widgets = {}

        self.focused_data_widget = urwid.Text('')
        self.body = urwid.Filler(urwid.Pile([urwid.Divider(), urwid.Text(('prompt_attr', 'FIELD DATA:')), self.focused_data_widget]), valign='top')

        self.status_bar = [urwid.Text(''), urwid.Text('')]
        self.footer = urwid.Pile([urwid.Divider(), urwid.Text(('prompt_attr', 'STATUS: '))] + self.status_bar)
        self._w = urwid.Frame(header=self.header, body=self.body, footer=self.footer, focus_part='body')

    # @property
    # def modified_record_dict(self):
    #     return self._modified_record_dict

    # @modified_record_dict.setter
    # def modified_record_dict(self, modified_record_dict):
    #     """
    #     when a record_dict is set to a new value, populate the field_data_widgets with new record data.  Record is None for a new/nonexistent record.
    #     """
    #     if modified_record_dict is None:
    #         self._modified_record_dict = {field: '' for field in params.FIELD_NAMES}
    #         # self.screen_state = 'edit'
    #     else:
    #         self._modified_record_dict = modified_record_dict

    #     self.field_data_widgets = {}
    #     for field in params.FIELD_NAMES:
    #         if params.FIELD_TYPES[field] in params.EDITABLE_TYPES and self.screen_state == 'edit':
    #             self.field_data_widgets[field] = urwid.Edit('', str(self.modified_record_dict[field]), multiline=True, allow_tab=True)
    #         else:
    #             self.field_data_widgets[field] = urwid.Text(str(self.modified_record_dict[field]))

    @property
    def screen_state(self):
        return self._screen_state

    @screen_state.setter
    def screen_state(self, screen_state):
        if screen_state not in {'display', 'edit', 'new'}:
            raise('Invalid select_screen.screen_state value.')
        self._screen_state = screen_state

    def create_modified_record_widgets(self, selected_record):

        for field in params.FIELD_NAMES:
            if params.FIELD_TYPES[field] in params.EDITABLE_TYPES:
                self.modified_record_widgets[field] = urwid.Edit('', str(selected_record[field]), multiline=True, allow_tab=True)
            else:
                self.modified_record_widgets[field] = urwid.Text(str(selected_record[field]))

    def create_new_record_widgets(self):

        for field in params.FIELD_NAMES:
            if params.FIELD_TYPES[field] in params.EDITABLE_TYPES:
                self.modified_record_widgets[field] = urwid.Edit('', '', multiline=True, allow_tab=True)
            else:
                self.modified_record_widgets[field] = urwid.Text('')

    def update_field_display(self, record, field_name):
        """
        # highlights the correct field widget
        # displays the field contents below
        """
        # self.title[0].set_text(('prompt_attr', str(record[params.SEARCH_DISPLAY_FIELD]).upper()))
        self.title[0].set_text(('prompt_attr', 'SELECTED RECORD'))

        field_text = str(record[field_name])
        for j, name in enumerate(params.FIELD_NAMES):
            if field_name == name:
                self.field_label_widgets[j].set_attr_map({None: 'selected_attr'})
            else:
                self.field_label_widgets[j].set_attr_map({None: 'unselected_attr'})

        if self.screen_state == 'display':
            self.body = urwid.Filler(urwid.Pile([urwid.Divider(), urwid.Divider(), urwid.Text(('prompt_attr', 'FIELD DATA:')), urwid.Text(field_text), self.focused_data_widget]), valign='top')

        if self.screen_state in {'edit', 'new'}:
            self.body = urwid.Filler(urwid.Pile([urwid.Divider(), urwid.Divider(), urwid.Text(('prompt_attr', 'FIELD DATA:')), self.modified_record_widgets[field_name], self.focused_data_widget]), valign='top')

        self._w = urwid.Frame(header=self.header, body=self.body, footer=self.footer, focus_part='body')

    def return_modified_record(self, selected_record):
        """
        creates an updated record_dict of editable record objects.  For use in updating a record in the app
        - results are not typed, but strings.  They are 
        typed at record update time.
        - unique/unmodifiable fields are not passed for updating a document, per documentation: http://whoosh.readthedocs.io/en/latest/api/writing.html?highlight=update_document
        """
        # import ipdb; ipdb.set_trace()
        modified_record_dict = dict()
        for field in params.FIELD_NAMES:
            f_type = type(selected_record[field])
            try:
                modified_record_dict[field] = f_type(self.modified_record_widgets[field].edit_text)
            except AttributeError:
                # update with uneditable
                # pass
                modified_record_dict[field] = selected_record[field]

        return modified_record_dict

    def update_status_bar(self, attr_text_tuples):
        """
        update footer/info at bottom of screen with tuples ('attribute', 'string')
        """
        self.status_bar = [urwid.Text((markup[0], markup[1])) for markup in attr_text_tuples]
        self.footer = urwid.Pile([urwid.Divider(), urwid.Text(('prompt_attr', 'STATUS: '))] + self.status_bar)
        self._w = urwid.Frame(header=self.header, body=self.body, footer=self.footer, focus_part='body')








if __name__ == '__main__':

    # n = 10       
    # focus_labels = ['selection {}'.format(j) for j in range(n)]

    my_widget = SelectScreen()
    palette = params.PALETTE

    urwid.MainLoop(my_widget, palette=palette).run()

#%%