#%%
import urwid
import config_files.default_config as params

class Observable_Edit(urwid.Edit):

    def __init__(self, *args, **kwargs):
        #'observer' callback functions:
        self._observers = []
        super().__init__(*args, **kwargs)

    def set_edit_text(self, text):
        """
        - overloads the urid.Edit.set_edit_text() method
        - executes callback functions stored in observers
        """
        super().set_edit_text(text)
        for callback in self._observers:
            callback(self.edit_text)

    def bind_to(self, callback):
        # binds function 'callback', a method in another class, to self._observers 
        self._observers.append(callback)

class SearchScreen(urwid.WidgetWrap):
    """
    arguments:  screen_state = {search, browse}
    query_str:  search string for document list
    labels:     ??s
    
    """
    def __init__(self, screen_state='search', query_str='*', results=None):

        self.screen_state = screen_state
        self.query_widget = Observable_Edit(('prompt_attr', 'QUERY: '), query_str)
        self.query_widget.edit_pos = 0
        self.header = urwid.Pile([self.query_widget, urwid.Divider(), urwid.Text(('prompt_attr', 'RESULTS:'))])

        if results is None:
            results = []

        self.search_pile = urwid.Pile([urwid.AttrMap(urwid.SelectableIcon(label, wrap=clip), 'unselected_attr', focus_map='selected_attr') for label in results])

        self.body = urwid.Filler(self.search_pile, valign='top')
        self.preview = [urwid.Text('') for j in params.FIELD_NAMES]
        self.status_bar = [urwid.Text(''), urwid.Text('')]
        self.footer = urwid.Pile([urwid.Divider(), urwid.Text(('prompt_attr', 'PREVIEW: ')), urwid.Divider()] + self.preview + [urwid.Divider(), urwid.Text(('prompt_attr', 'STATUS: '))] + self.status_bar)

        self._w = urwid.Frame(header=self.header, body=self.body, footer=self.footer, focus_part='header')
        # self.search_focus = 0
        self.update_preview()

    @property
    def query_str(self):
        return self.query_widget.edit_text

    @property
    def search_focus(self):

        try:
            return self.search_pile.focus_position
        except IndexError:
            return 0

    @search_focus.setter
    def search_focus(self, index_val):

        try:
            #stop if there are no results
            self.search_pile.focus_item.set_attr_map({None: 'unselected_attr'})
        except AttributeError:
            return
        try:
            self.search_pile.focus_position = index_val
        except IndexError:
            pass

        self.search_pile.focus_item.set_attr_map({None: 'selected_attr'})

    def update_records_display(self, results, selected_record):
        """
        Updates screen with list of widgets (results); selected_record will be highlighted if present.

        Can be optimized to update the selected_record only as needed.
        """
        preview_field = params.SEARCH_DISPLAY_FIELD
        results_list = []
        for result in results:
            result_str = '{}'.format(result[preview_field])

            results_list.append(urwid.AttrMap(urwid.SelectableIcon(result_str), 'unselected_attr', focus_map='unselected_attr'))

            if result == selected_record:
                results_list[-1].set_attr_map({None: 'selected_attr'})

        self.search_pile = urwid.Pile(results_list)
        self.body = urwid.Filler(self.search_pile, valign='top')
        self._w = urwid.Frame(header=self.header, body=self.body, footer=self.footer, focus_part='header')

    def update_focus_record(self, results, selected_record):
        """
        Updates screen with list of widgets (results); selected_record will be highlighted if present.
        Can be optimized to update the selected_record only as needed.
        """
        for j, result in enumerate(results):
            if selected_record[params.UNIQUE_FIELD] == results[j].fields()[params.UNIQUE_FIELD]:

                # widget[j].set_attr_map({None: 'selected_attr'})
                self.search_pile.base_widget.contents[j][0].set_attr_map({None: 'selected_attr'})

        self.body = urwid.Filler(self.search_pile, valign='top')
        self._w = urwid.Frame(header=self.header, body=self.body, footer=self.footer, focus_part='header')

    def update_preview(self, selected_record=None):
        """
        updates preview of selected_record
        """
        # field_strs = str(value).split('\n')[0]
        field_strs = [('prompt_attr', '{:13}'.format(field)) for field in params.FIELD_NAMES]
        if not selected_record:
            data_strs = ['' for name in params.FIELD_NAMES]
        else:
            data_strs = [('unselected_attr', str(selected_record[field]).split('\n')[0]) for field in params.FIELD_NAMES]
        self.preview = [urwid.Text([field, data] , wrap='clip') for field, data in zip(field_strs, data_strs)]

        # self.preview = [urwid.Text(('unselected_attr', str(result[field])), wrap='clip') for field in params.FIELD_NAMES]
        self.footer = urwid.Pile([urwid.Divider(), urwid.Text(('prompt_attr', 'PREVIEW:')), urwid.Divider()] + self.preview + [urwid.Divider(), urwid.Text(('prompt_attr', 'STATUS: '))] + self.status_bar)
        self._w.set_footer(self.footer)

    def update_status_bar(self, attr_text_tuples):
        """
        update footer/info at bottom of screen with tuples ('attribute', 'string')
        """
        # import ipdb; ipdb.set_trace()
        self.status_bar = [urwid.Text((markup[0], markup[1])) for markup in attr_text_tuples]
        # import ipdb; ipdb.set_trace()
        self.footer = urwid.Pile([urwid.Divider(), urwid.Text(('prompt_attr', 'PREVIEW: ')), urwid.Divider()] + self.preview + [urwid.Divider(), urwid.Text(('prompt_attr', 'STATUS: '))] + self.status_bar)

        self._w = urwid.Frame(header=self.header, body=self.body, footer=self.footer, focus_part='header')

if __name__ == '__main__':
    import sys
    sys.stdout.write('(add brief example to demonstrate search_screen.py)\n')
