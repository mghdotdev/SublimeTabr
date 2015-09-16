import sublime
import sublime_plugin

tabberActive = False
tabberSelections = []
tabberSelectionCounter = 0
tabberCharacterCount = -1

class TabberCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		global tabberSelections
		global tabberActive
		global tabberSelectionCounter
		global tabberCharacterCount

		tabberActive = False
		tabberSelections = []
		tabberSelectionCounter = 0
		tabberCharacterCount = -1

		selections = self.view.sel()
		
		for region in selections:

			tabberSelections.append([region.begin(), region.begin()])
			self.view.replace(edit, region, '')

		self.view.sel().clear()
		self.view.sel().add(sublime.Region(tabberSelections[0][0]))

		print(tabberSelections)

		tabberActive = True

class TabberTabHandler(sublime_plugin.EventListener):
	def on_query_context(self, view, key, operator, operand, match_all):

		global tabberActive

		if key == 'tabber_tab' and tabberActive == True:
			return True

class TabberDeleteHandler(sublime_plugin.EventListener):
	def on_query_context(self, view, key, operator, operand, match_all):

		global tabberActive
		global tabberCharacterCount

		print(key)

		if (key == 'tabber_delete' or key == 'tabber_backspace') and tabberActive == True:
			tabberCharacterCount -= 2;

class TabberGotoNextCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		global tabberSelections
		global tabberSelectionCounter
		global tabberActive
		global tabberCharacterCount

		tabberCharacterCount = 0
		tabberSelectionCounter += 1

		print(tabberSelections)

		if tabberSelectionCounter < len(tabberSelections):
			self.view.sel().clear()
			self.view.sel().add(sublime.Region(tabberSelections[tabberSelectionCounter][1]))
		else:
			tabberActive = False

class TabberGotoPreviousCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		""

class TabberCountCommand(sublime_plugin.EventListener):
	def on_modified(self, view):

		global tabberCharacterCount
		global tabberSelectionCounter

		tabberCharacterCount += 1
		tabberSelections[tabberSelectionCounter][1] = tabberCharacterCount