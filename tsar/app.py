#!/usr/bin/env python
import urwid
import sys
import whoosh
from search_screen import SearchScreen
from select_screen import SelectScreen
import config_files.default_config as params
from copy import copy
from datetime import datetime
from whoosh import writing

class App(urwid.WidgetWrap):

    """
    descr.
    """
    def __init__(self,
                 params=None,
                 active_screen=None,
                 search_index=None,
                 parser=None,
                 screen_list=None,
                 search_results=None,
                 ):

        self.query_str = ''
        self.results = []

        self.params = params
        self.search_index = search_index
        self.searcher = self.search_index.searcher()
        self.parser = parser

        self.screen_list = screen_list
        self._screen_by_type_dict = {type(screen): screen for screen in self.screen_list}
        self.selected_record = None
        self.modified_record = None
        self.new_record = None
        # results, query_str, selected_record set set from search_screen 

        #init methods:
        if active_screen is None:
            self.active_screen = self.screen_list[0]
        self.search_screen.update_records_display(results=self.results, selected_record=self.selected_record)
        self.search_screen.update_preview(selected_record=self.selected_record)
        self.selected_field = params.FIELD_NAMES[0]
        self.search_screen.query_widget.bind_to(self.update_query)
        self.update_query(self.search_screen.query_str)

        self.search_screen.update_records_display(self.results, self.selected_record)
        self.search_screen.update_preview(self.selected_record)
        self.search_screen.update_status_bar([('default', 'showing {} of {} results'.format(len(self.results), self.search_index.doc_count())), ('default', '')])

    @property
    def selected_record(self):
        # returns a dict of the selected record
        # if there are no results, return None
        if not self.results:
            # return None
            return {field: None for field in self.search_index.schema.names()}

        if self._selected_record in list(self.results):
            return self._selected_record
            # return self._selected_record.fields()

        if self._selected_record not in list(self.results):
            self._selected_record = self.results[0]

            return self._selected_record

    @selected_record.setter
    def selected_record(self, record):
        # if there are no results, return None
        # if record doesn't exist, return first
        # set _selected_record to desired record
        # _selected record is type <Hit>
        # self.selected_field = params.FIELD_NAMES[0]
        if not self.results:
            # self._selected_record = None
            self._selected_record = {field: None for field in self.search_index.schema.names()}
            return

        if record not in list(self.results):
            self._selected_record = self.results[0]
            return
        self._selected_record = record

    @property
    def selected_field(self):
        return self._selected_field

    @selected_field.setter
    def selected_field(self, field):
        """
        - set selected_field from params.FIELD_NAMES
        - selected_field is reset when selected_record changes
        """
        self._selected_field = field
        if field not in params.FIELD_NAMES:
            raise Exception('field name does not exist in current schema')

    def update_query(self, query_str):
        self.query_str = query_str
        self.searcher = self.searcher.refresh()
        query = self.parser.parse(self.query_str)
        self.results = self.searcher.search(query, limit=self.params.SEARCH_RESULT_LIMIT, sortedby=params.UNIQUE_FIELD)

    def select_previous_field(self):
        # update selected_field with previous field
        fields_list = params.FIELD_NAMES
        try:
            ind = fields_list.index(self.selected_field)
        except ValueError:
            self.selected_field = None
            return
        if ind > 0:
            self.selected_field = fields_list[ind - 1]

    def select_next_field(self):
        # update selected_field with next field
        fields_list = params.FIELD_NAMES
        try:
            ind = fields_list.index(self.selected_field)
        except ValueError:
            self.selected_field = None
            return
        if ind < len(fields_list) - 1:
            self.selected_field = fields_list[ind + 1]

    def select_previous_record(self):
        # if record is not in results, return None
        # this is converted to first result, or None by @property selected_record
        # if record is not first, set to prev record
        # if record is first, do nothing
        results_list = list(self.results)
        try:
            ind = results_list.index(self.selected_record)
        except ValueError:
            self.selected_record = None
            return
        if ind > 0:
            self.selected_record = results_list[ind - 1]

    def select_next_record(self):
        # if record is not in results, return None
        # this is converted to first result, or None by @property selected_record
        # if record is not last, set to next record
        # if record is last, do nothing
        results_list = list(self.results)
        try:
            ind = results_list.index(self.selected_record)
        except ValueError:
            self.selected_record = None
            return
        if ind < len(results_list) - 1:
            self.selected_record = results_list[ind + 1]

    @property
    def search_screen(self):
        return self._screen_by_type_dict[SearchScreen]

    @property
    def select_screen(self):
        return self._screen_by_type_dict[SelectScreen]

    @property
    def active_screen(self):
        return self._w

    @active_screen.setter
    def active_screen(self, active_screen):
        """
        active screen is a widget object.  Some UI bits are 'refreshed', as an example:
        """
        try:
            self._w = active_screen
        except ValueError:
            print('error in active_screen')
        if active_screen == self.search_screen:
            #modify search_screen results, etc
            # self.search_screen.display_query_results(self.results)
            # self.search_screen.update_records_display(self.results, self.selected_record)
            # self.search_screen.update_preview(self.results)
            pass
        if active_screen == self.select_screen:
            #update select_screen interface
            pass

    # @state_history_setter
    # def state_history(self):
    #     #record the state history of the app

    def keypress(self, size, key):
        """
        Handles keystrokes at the app level that require changing the screen state.
        """

        if key == 'esc':
            raise urwid.ExitMainLoop()

        if self.active_screen == self.search_screen and self.search_screen.screen_state == 'search':

            if key == 'up':
                self.select_previous_record()
                self.search_screen.update_records_display(results=self.results, selected_record=self.selected_record)
                self.search_screen.update_preview(self.selected_record)
                self.search_screen.update_status_bar([('default', 'showing {} of {} results'.format(len(self.results), self.search_index.doc_count())), ('default', '')])
                return

            if key == 'down':
                self.select_next_record()
                self.search_screen.update_records_display(results=self.results, selected_record=self.selected_record)
                self.search_screen.update_preview(self.selected_record)
                self.search_screen.update_status_bar([('default', 'showing {} of {} results'.format(len(self.results), self.search_index.doc_count())), ('default', '')])
                return

            if key == 'enter':
                # change current_screen to focus_screen (display mode)
                # populate with selected_record
                if self.selected_record[params.UNIQUE_FIELD] is None:
                    self.search_screen.update_status_bar([('default', 'showing {} of {} results'.format(len(self.results), self.search_index.doc_count())), ('selected_attr', 'no result to display')])
                    return

                self.active_screen = self.select_screen
                self.select_screen.screen_state = 'display'
                self.select_screen.update_field_display(self.selected_record, self.selected_field)
                self.select_screen.update_status_bar([('default', ''), ('default', 'DISPLAYING SELECTED RECORD')])

                return

            if key == 'ctrl d':
                # delete selected_record from index
                # update search_screen interface
                writer = self.search_index.writer()
                writer.delete_document(self.selected_record.docnum)
                writer.commit()
                self.update_query(self.search_screen.query_str)        
                self.search_screen.update_records_display(results=self.results, selected_record=self.selected_record)
                self.search_screen.update_preview(self.selected_record)
                self.search_screen.update_status_bar([('default', 'showing {} of {} results'.format(len(self.results), self.search_index.doc_count())), ('selected_attr', 'RECORD PERMANENTLY REMOVED')])
                return

            if key == 'ctrl x':
                self.search_screen.update_status_bar([('default', 'showing {} of {} results'.format(len(self.results), self.search_index.doc_count())), ('default', 'NOTHING TO CANCEL')])
                return

            if key == 'ctrl u':

                if self.selected_record[params.UNIQUE_FIELD] is None:
                    self.search_screen.update_status_bar([('default', 'showing {} of {} results'.format(len(self.results), self.search_index.doc_count())), ('selected_attr', 'no result to edit')])
                    return
                self.active_screen = self.select_screen
                self.select_screen.screen_state = 'edit'
                self.select_screen.create_modified_record_widgets(self.selected_record)
                self.select_screen.update_field_display(self.selected_record, self.
                    selected_field)
                self.select_screen.update_status_bar([
                    ('', ''),
                    ('selected_attr', 'EDITING SELECTED RECORD')])
                return

            if key == 'ctrl n':

                self.active_screen = self.select_screen
                self.select_screen.screen_state = 'new'
                self.select_screen.create_new_record_widgets()
                # import ipdb; ipdb.set_trace()
                self.select_screen.update_field_display(self.selected_record, self.selected_field)
                self.select_screen.update_status_bar([
                    ('', ''),
                    ('selected_attr', 'NEW RECORD')])
                return

            # else keystrokes go to search query
            super().keypress(size, key)
            self.search_screen.update_records_display(results=self.results, selected_record=self.selected_record)
            self.search_screen.update_preview(self.selected_record)
            self.search_screen.update_status_bar([('default', 'showing {} of {} results'.format(len(self.results), self.search_index.doc_count())), ('default', '')])

            return

        if self.active_screen == self.search_screen and self.search_screen.screen_state == 'browse':
            pass

        if self.active_screen == self.select_screen and self.select_screen.screen_state == 'display':

            if key == 'up':
                self.select_previous_field()
                self.select_screen.update_field_display(self.selected_record, self.selected_field)
                self.select_screen.update_status_bar([('default', ''), ('default', 'DISPLAYING SELECTED RECORD')])
                return

            if key == 'down':
                self.select_next_field()
                self.select_screen.update_field_display(self.selected_record, self.selected_field)
                self.select_screen.update_status_bar([('default', ''), ('default', 'DISPLAYING SELECTED RECORD')])
                return

            if key == 'enter':
                # change active_screen to search
                self.active_screen = self.search_screen
                return

            if key == 'ctrl x':
                self.select_screen.update_status_bar([('', ''), ('default', 'NOTHING TO CANCEL')])
                return

            if key == 'ctrl d':
                # remove selected_record
                # update query/records
                # go to search_screen
                writer = self.search_index.writer()
                # import ipdb; ipdb.set_trace()
                writer.delete_document(self.selected_record.docnum)
                writer.commit()
                self.update_query(self.search_screen.query_str)

                self.search_screen.update_records_display(results=self.results, selected_record=self.selected_record)
                self.search_screen.update_preview(self.selected_record)
                self.active_screen = self.search_screen
                self.search_screen.update_status_bar([('default', 'showing {} of {} results'.format(len(self.results), self.search_index.doc_count())), ('selected_attr', 'RECORD PERMANENTLY REMOVED')])
                return

            if key == 'ctrl n':
                self.select_screen.screen_state = 'new'
                self.select_screen.create_new_record_widgets()
                self.select_screen.update_field_display(self.selected_record, self.selected_field)
                self.select_screen.update_status_bar([
                    ('default', ''),
                    ('selected_attr', 'NEW RECORD')])
                return

            if key == 'ctrl u':
                self.select_screen.screen_state = 'edit'
                self.select_screen.create_modified_record_widgets(self.selected_record)
                self.select_screen.update_field_display(self.selected_record, self.selected_field)
                self.select_screen.update_status_bar([
                    ('default', ''),
                    ('selected_attr', 'EDITING SELECTED RECORD')])
                return

            # other keystrokes do nothing
            # super().keypress(size, key)
            return

        if self.active_screen == self.select_screen and self.select_screen.screen_state in {'edit', 'new'}:

            if key == 'up':
                self.select_previous_field()
                self.select_screen.update_field_display(self.selected_record, self.selected_field)
                if self.select_screen.screen_state == 'edit':
                    self.select_screen.update_status_bar([('default', ''), ('selected_attr', 'EDITING SELECTED RECORD')])
                if self.select_screen.screen_state == 'new':
                    self.select_screen.update_status_bar([('default', ''), ('selected_attr', 'NEW RECORD')])
                return

            if key == 'down':
                self.select_next_field()
                self.select_screen.update_field_display(self.selected_record, self.selected_field)
                if self.select_screen.screen_state == 'edit':
                    self.select_screen.update_status_bar([('default', ''), ('selected_attr', 'EDITING SELECTED RECORD')])
                if self.select_screen.screen_state == 'new':
                    self.select_screen.update_status_bar([('default', ''), ('selected_attr', 'NEW RECORD')])

                return

            if key == 'ctrl up':
                # move cursor up in multiline edit text
                key = 'up'

            if key == 'ctrl down':
                # move cursor down in multiline edit text
                key = 'down'

            if key == 'ctrl n':
                # update footer: 'save or cancel edits before creating a new file'
                self.select_screen.update_status_bar([('default', ''), ('selected_attr', 'SAVE EDITS (ctrl u) OR CANCEL (ctrl x)')])
                return

            if key == 'ctrl u':

                modified_record_dict = self.select_screen.return_modified_record(self.selected_record)
                if self.select_screen.screen_state == 'new':
                    # add creation timestamp
                    for k, v in modified_record_dict.items():
                        if isinstance(v, datetime):
                            modified_record_dict[k] = datetime.now()

                writer = self.search_index.writer()
                writer.update_document(**modified_record_dict)
                writer.commit()
                self.searcher = self.searcher.refresh()
                self.update_query(self.search_screen.query_str)
                self.selected_record = self.searcher.document(**{params.UNIQUE_FIELD:modified_record_dict[params.UNIQUE_FIELD]})
                self.select_screen.screen_state = 'display'
                self.select_screen.update_field_display(self.selected_record, self.selected_field)
                self.search_screen.update_records_display(self.results, self.selected_record)
                self.search_screen.update_focus_record(self.results, self.selected_record)
                self.search_screen.update_preview(self.selected_record)
                self.select_screen.update_status_bar([('default', ''), ('default', 'DISPLAYING SELECTED RECORD')])
                return

            if key == 'ctrl x':
                # cancel updates; populate previously stored record
                if self.select_screen.screen_state == 'edit':
                    self.select_screen.screen_state = 'display'
                    self.select_screen.update_field_display(self.selected_record, self.selected_field)
                    self.search_screen.update_records_display(self.results, self.selected_record)
                    self.select_screen.update_status_bar([('default', ''), ('default', 'EDITS CANCELED')])
                    return

                if self.select_screen.screen_state == 'new':
                    self.select_screen.screen_state = 'display'
                    self.select_screen.update_field_display(self.selected_record, self.selected_field)
                    self.search_screen.update_records_display(self.results, self.selected_record)
                    self.search_screen.update_status_bar([('default', ''), ('default', 'EDITS CANCELED')])
                    self.active_screen = self.search_screen
                    return

            if key == 'ctrl d':
                self.select_screen.update_status_bar([('default', ''), ('selected_attr', 'SAVE EDITS (ctrl u) OR CANCEL (ctrl x)')])
                return
                pass

            # other keystrokes edit current field
            super().keypress(size, key)
            return


if __name__ == '__main__':

    print('look at tsar.py to fix me')
    # from search_screen import SearchScreen
    # from focus_screen import FocusScreen
    # search_screen = SearchScreen()

    # app = App(screen_list=[search_screen])
