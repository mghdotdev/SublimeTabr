import sublime
import sublime_plugin

# Define Global Variables
TabberVariables = {
	'tabberActive': False,
	'tabberSelections': [],
	'tabberCurrentSelection': 0,
	'viewSize': 0	
}

class TabberCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		global TabberVariables

		# Grab Intial Selections
		selections = self.view.sel()

		# Reset Selections Array
		TabberVariables['tabberSelections'] = []
		
		# Create Data Structure
		for region in selections:
			TabberVariables['tabberSelections'].append({
				'start': region.begin(),
				'end': region.begin(),
				'difference': 0
			})
			self.view.replace(edit, region, '')

		# Clear / Place Cursor to First Selection
		self.view.sel().clear()
		self.view.sel().add(sublime.Region(TabberVariables['tabberSelections'][0]['start']))

		# Set Globals
		TabberVariables['tabberActive'] = True
		TabberVariables['tabberCurrentSelection'] = 0
		TabberVariables['viewSize'] = self.view.size()

class TabberEscapeHandler(sublime_plugin.EventListener):
	def on_query_context(self, view, key, operator, operand, match_all):

		global TabberVariables

		if key == 'tabber_escape' and TabberVariables['tabberActive'] == True:
			return True

class TabberExitCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		global TabberVariables

		TabberVariables['tabberActive'] = False
		TabberVariables['tabberSelections'] = []
		TabberVariables['tabberCurrentSelection'] = 0
		TabberVariables['viewSize'] = 0

class TabberTabHandler(sublime_plugin.EventListener):
	def on_query_context(self, view, key, operator, operand, match_all):

		global TabberVariables

		if key == 'tabber_tab' and TabberVariables['tabberActive'] == True:
			return True

class TabberGotoNextCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		global TabberVariables

		TabberVariables['tabberCurrentSelection'] += 1

		print(TabberVariables['tabberCurrentSelection'], len(TabberVariables['tabberSelections']))

		offset = 0
		for x in range(0, TabberVariables['tabberCurrentSelection']):
			offset += TabberVariables['tabberSelections'][x]['difference']

		if TabberVariables['tabberCurrentSelection'] < len(TabberVariables['tabberSelections']):
			self.view.sel().clear()
			self.view.sel().add( sublime.Region( TabberVariables['tabberSelections'][TabberVariables['tabberCurrentSelection']]['start'] + offset ) )
			
			# Reset View Size
			TabberVariables['viewSize'] = self.view.size()
			
			if (TabberVariables['tabberCurrentSelection'] + 1) == len(TabberVariables['tabberSelections']):
				TabberVariables['tabberActive'] = False
				TabberVariables['tabberSelections'] = []
				TabberVariables['tabberCurrentSelection'] = 0
				TabberVariables['viewSize'] = 0

class TabberGotoPreviousCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		global TabberVariables

		# NEEDS TO BE SOLVED
		

class TabberCountCommand(sublime_plugin.EventListener):
	def on_modified(self, view):

		global TabberVariables

		if (len(TabberVariables['tabberSelections']) > 0):
			TabberVariables['tabberSelections'][TabberVariables['tabberCurrentSelection']]['end'] = TabberVariables['tabberSelections'][TabberVariables['tabberCurrentSelection']]['end'] + view.size() - TabberVariables['viewSize']
			TabberVariables['tabberSelections'][TabberVariables['tabberCurrentSelection']]['difference'] = view.size() - TabberVariables['viewSize']