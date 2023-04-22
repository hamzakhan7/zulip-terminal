from collections import OrderedDict

import pytest
import random
import string
from urwid import Divider

from zulipterminal.config.keys import keys_for_command, primary_key_for_command
from zulipterminal.config.symbols import STATUS_ACTIVE
from zulipterminal.helper import powerset
from zulipterminal.ui_tools.views import (
    SIDE_PANELS_MOUSE_SCROLL_LINES,
    LeftColumnView,
    MessageView,
    MiddleColumnView,
    ModListWalker,
    RightColumnView,
    StreamsView,
    StreamsViewDivider,
    TabView,
    TopicsView,
    UsersView,
)

SUBDIR = "zulipterminal.ui_tools"
VIEWS = SUBDIR + ".views"
MESSAGEVIEW = VIEWS + ".MessageView"
MIDCOLVIEW = VIEWS + ".MiddleColumnView"

class TestIssue():
    @pytest.fixture(autouse=True)
    def mock_external_classes(self, mocker):
        self.model = mocker.MagicMock()
        self.view = mocker.Mock()
        self.urwid = mocker.patch(VIEWS + ".urwid")

    @pytest.fixture
    def msg_view(self, mocker, msg_box):
        mocker.patch(MESSAGEVIEW + ".main_view", return_value=[msg_box])
        mocker.patch(MESSAGEVIEW + ".read_message")
        mocker.patch(MESSAGEVIEW + ".set_focus")
        msg_view = MessageView(self.model, self.view)
        msg_view.log = mocker.Mock()
        msg_view.body = mocker.Mock()
        return msg_view
    
    @pytest.mark.parametrize("narrow_focus_pos, focus_msg", [(set(), 1), (0, 9999999)])
    def test_main_view_issue1226(self, mocker, narrow_focus_pos, focus_msg):
        print("focused message " + str(focus_msg))

        mocker.patch(MESSAGEVIEW + ".read_message")
        self.urwid.SimpleFocusListWalker.return_value = mocker.Mock()
        mocker.patch(MESSAGEVIEW + ".set_focus")
        msg_list = []
        # making large message list
        for i in range(10000000):
            msg_list.append("MSG" + str(i))

        mocker.patch(VIEWS + ".create_msg_box_list", return_value=msg_list)
        self.model.get_focus_in_current_narrow.return_value = narrow_focus_pos

        msg_view = MessageView(self.model, self.view)

        # assert msg_view.focus_msg == focus_msg
