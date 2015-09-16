import sublime
import sublime_plugin

TabberSelections = []
TabberSelectionCounter = 0
TabberActive = False

class TabberCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		global TabberSelections
		global TabberActive
		global TabberSelectionCounter

		TabberSelections = []
		TabberSelectionCounter = 0

		selections = self.view.sel()
		
		for region in selections:

			TabberSelections.append([region.begin(), region.end()])
			self.view.replace(edit, region, '')

		self.view.sel().clear()
		self.view.sel().add(sublime.Region(TabberSelections[0][0]))

		TabberActive = True

class TabberTabHandler(sublime_plugin.EventListener):
	def on_query_context(self, view, key, operator, operand, match_all):

		global TabberActive

		if key == 'tabber' and TabberActive == True:
			return True

class TabberGotoNextCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		global TabberSelections
		global TabberSelectionCounter
		global TabberActive

		TabberSelectionCounter += 1;

		if TabberSelectionCounter < len(TabberSelections):
			self.view.sel().clear()
			self.view.sel().add(sublime.Region(TabberSelections[TabberSelectionCounter][0]))
		else:
			TabberActive = False

class TabberGotoPreviousCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		global TabberSelections
		global TabberSelectionCounter
		global TabberActiveW

		TabberSelectionCounter -= 1;

		print(TabberSelectionCounter)

		if TabberSelectionCounter < len(TabberSelections) and TabberSelectionCounter > -1:
			self.view.sel().clear()
			self.view.sel().add(sublime.Region(TabberSelections[TabberSelectionCounter][0]))
		else:
			TabberSelectionCounter = 0