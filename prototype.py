#!/usr/bin/python
# -*- coding: utf-8 -*-

# newclass.py

import wx
import urllib2
import json


class BarkManager:

    zid = ''
    token = ''

    def authenticate(self, username, password):
        return True

    def set_token(self, token):
        self.token = token

    def get_token(self):
        return self.token

    def set_user(self, zid):
        self.zid = zid

    def check_in(self, max_scans):
        if not self.token:
            return False

        data = json.dumps({
            'token': self.token,
            'action': 'check_in',
            'zid': self.zid,
            'max_scans': max_scans,
        })
        url = 'https://bark.csesoc.unsw.edu.au/api'
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
        resp = urllib2.urlopen(req).read()
        return json.loads(resp)

    def set_arc(self, is_arc):
        if not self.token:
            return False

        data = json.dumps({
            'token': self.token,
            'action': 'update_arc',
            'zid': self.zid,
            'is_arc': is_arc,
        })

        print data
        url = 'https://bark.csesoc.unsw.edu.au/api'
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
        resp = urllib2.urlopen(req).read()
        return json.loads(resp)['success']

    def get_event(self):
        if not self.token:
            return False

        data = json.dumps({
            'token': self.token,
            'action': 'get_event_info',
        })
        print data
        url = 'https://bark.csesoc.unsw.edu.au/api'
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
        resp = urllib2.urlopen(req).read()
        json_resp = json.loads(resp)
        if json_resp['success']:
            self.event_name = json_resp['name']
            return True
        return False



class LoginWindow(wx.Frame):

    def __init__(self, parent, bm):
        super(LoginWindow, self).__init__(parent, size=(320, 240))
        self.bm = bm

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(5, 5)

        self.header = wx.StaticText(panel, label="Login to Bark")
        sizer.Add(self.header, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM,
                  border=15)

        self.line = wx.StaticLine(panel)
        sizer.Add(self.line, pos=(1, 0), span=(1, 5), flag=wx.EXPAND | wx.BOTTOM,
                  border=10)

        # self.zid_label = wx.StaticText(panel, label="zID")
        # sizer.Add(self.zid_label, pos=(2, 0), flag=wx.LEFT, border=10)
        #
        # self.zid = wx.TextCtrl(panel)
        # sizer.Add(self.zid, pos=(2, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND)
        #
        # self.password_label = wx.StaticText(panel, label="Password")
        # sizer.Add(self.password_label, pos=(3, 0), flag=wx.LEFT | wx.TOP, border=10)
        #
        # self.password = wx.TextCtrl(panel)
        # sizer.Add(self.password, pos=(3, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND,
        #           border=5)

        self.token_label = wx.StaticText(panel, label="Token")
        sizer.Add(
            self.token_label, pos=(4, 0), flag=wx.LEFT | wx.TOP, border=10)

        self.token = wx.TextCtrl(panel)
        sizer.Add(self.token, pos=(4, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND,
                  border=5)

        self.login = wx.Button(panel, label="Login")
        sizer.Add(self.login, pos=(5, 3), span=(1, 1), flag=wx.BOTTOM | wx.RIGHT,
                  border=5)

        sizer.AddGrowableCol(2)

        panel.SetSizer(sizer)

        # Set event handlers
        self.login.Bind(wx.EVT_BUTTON, self.Login)

    def Login(self, e):
        # if self.bm.authenticate(self.zid.GetValue(), self.password.GetValue()):
            #self.bm.check_in('z3463754', 2)
        self.bm.set_token(self.token.GetValue())
        if self.bm.get_token():
            if self.bm.get_event():
                self.Close()
                CheckInWindow(None, self.bm)


class CheckInWindow (wx.Frame):

    def __init__(self, parent, bm):
        self.bm = bm
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=wx.Size(
            320, 250), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.InitUI()
        self.Center()
        self.Show()

    def InitUI(self):
        b_sizer = wx.BoxSizer(wx.VERTICAL)

        sizer = wx.FlexGridSizer(5, 1, 0, 0)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(4)
        sizer.SetFlexibleDirection(wx.BOTH)
        sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.header = wx.StaticText(
            self, wx.ID_ANY, u"Bark Check In (%s)" % self.bm.event_name, wx.DefaultPosition, wx.DefaultSize, 0)
        self.header.Wrap(-1)
        font = wx.Font(18, wx.NORMAL, wx.NORMAL, wx.BOLD)
        self.header.SetFont(font)
        sizer.Add(self.header, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.line = wx.StaticLine(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer.Add(self.line, 0, wx.EXPAND | wx.ALL, 5)

        self.zid = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER)
        sizer.Add(self.zid, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.line2 = wx.StaticLine(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer.Add(self.line2, 0, wx.EXPAND | wx.ALL, 5)

        self.result = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                  wx.DefaultSize, wx.TE_MULTILINE | wx.TE_NO_VSCROLL | wx.TE_READONLY)
        sizer.Add(self.result, 0, wx.ALL | wx.EXPAND, 5)

        b_sizer.Add(sizer, 1, wx.EXPAND, 5)

        self.SetSizer(b_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.zid.Bind(wx.EVT_TEXT_ENTER, self.check_in)

    # Virtual event handlers, overide them in your derived class
    def check_in(self, event):
        self.bm.set_user(self.zid.GetValue())
        self.zid.SetValue('')
        self.result.SetValue('')
        result = self.bm.check_in(4)
        print result
        if result['success']:
            if result['is_cse']:
                self.result.AppendText("Name: %s\n" % result['name'])
                self.result.AppendText("Degree: %s\n" % result['degree'])
                self.result.AppendText("Courses: %s\n" % ' '.join(result['courses']))

                self.result.SetBackgroundColour((139, 195, 74))
            else:
                self.result.SetValue("Not CSE")
                self.result.SetBackgroundColour((244, 67, 54))

            if not result['is_arc']:
                dlg = wx.MessageDialog(self,
                                       "Are you an Arc member?",
                                       "Confirm Arc Membership", style=wx.YES_NO)
                result = dlg.ShowModal()
                dlg.Destroy()
                if self.bm.zid:
                    if result == wx.ID_YES:
                        self.bm.set_arc(True)
                    elif result == wx.ID_NO:
                        self.bm.set_arc(False)
                else:
                    print "zID missing"
        else:
            self.result.SetValue(result['error'])
            self.result.SetBackgroundColour((255, 193, 7))
        event.Skip()


if __name__ == '__main__':
    app = wx.App()
    bm = BarkManager()
    f = LoginWindow(None, bm)
    app.MainLoop()
