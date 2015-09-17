import sublime
import sublime_plugin

# Define Global Variables
tabberActive = False
tabberSelections = []
tabberCurrentSelection = 0
viewSize = 0

class TabberCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		global tabberActive
		global tabberSelections
		global tabberCurrentSelection
		global viewSize

		# Grab Intial Selections
		selections = self.view.sel()

		# Reset Selections Array
		tabberSelections = []
		
		# Create Data Structure
		for region in selections:
			tabberSelections.append({
				'start': region.begin(),
				'end': region.begin(),
				'difference': 0
			})
			self.view.replace(edit, region, '')

		# Clear / Place Cursor to First Selection
		self.view.sel().clear()
		self.view.sel().add(sublime.Region(tabberSelections[0]['start']))

		# Set Globals
		tabberActive = True
		tabberCurrentSelection = 0
		viewSize = self.view.size();

class TabberTabHandler(sublime_plugin.EventListener):
	def on_query_context(self, view, key, operator, operand, match_all):

		global tabberActive

		if key == 'tabber_tab' and tabberActive == True:
			return True

class TabberGotoNextCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		global tabberActive
		global tabberSelections
		global tabberCurrentSelection
		global viewSize

		# print(tabberSelections)

		tabberCurrentSelection += 1

		offset = 0
		for x in range(0, tabberCurrentSelection):
			offset += tabberSelections[x]['difference']

		if tabberCurrentSelection < len(tabberSelections):
			self.view.sel().clear()
			self.view.sel().add( sublime.Region( tabberSelections[tabberCurrentSelection]['start'] + offset ) )
		else:
			tabberActive = False
			tabberSelections = []

		# Reset View Size
		viewSize = self.view.size()

class TabberGotoPreviousCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		global tabberActive
		global tabberSelections
		global tabberCurrentSelection
		global viewSize

		# NEEDS TO BE SOLVED

class TabberCountCommand(sublime_plugin.EventListener):
	def on_modified(self, view):

		global tabberCurrentSelection
		global viewSize

		if (len(tabberSelections) > 0):
			tabberSelections[tabberCurrentSelection]['end'] = tabberSelections[tabberCurrentSelection]['end'] + view.size() - viewSize
			tabberSelections[tabberCurrentSelection]['difference'] = view.size() - viewSize