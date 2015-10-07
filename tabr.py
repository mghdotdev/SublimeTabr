import sublime
import sublime_plugin

# Define Global Variables
TabrVariables = {
	'TabrActive': False,
	'TabrSelections': [],
	'TabrCurrentSelection': 0,
	'viewSize': 0	
}

class TabrCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		global TabrVariables

		# Grab Intial Selections
		selections = self.view.sel()

		# Reset Selections Array
		TabrVariables['TabrSelections'] = []
		
		# Create Data Structure
		for region in selections:
			TabrVariables['TabrSelections'].append({
				'start': region.begin(),
				'end': region.begin(),
				'difference': 0
			})
			self.view.replace(edit, region, '')

		# Clear / Place Cursor to First Selection
		self.view.sel().clear()
		self.view.sel().add(sublime.Region(TabrVariables['TabrSelections'][0]['start']))

		# Set Globals
		TabrVariables['TabrActive'] = True
		TabrVariables['TabrCurrentSelection'] = 0
		TabrVariables['viewSize'] = self.view.size()

class TabrEscapeHandler(sublime_plugin.EventListener):
	def on_query_context(self, view, key, operator, operand, match_all):

		global TabrVariables

		if key == 'Tabr_escape' and TabrVariables['TabrActive'] == True:
			return True

class TabrExitCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		global TabrVariables

		TabrVariables['TabrActive'] = False
		TabrVariables['TabrSelections'] = []
		TabrVariables['TabrCurrentSelection'] = 0
		TabrVariables['viewSize'] = 0

class TabrTabHandler(sublime_plugin.EventListener):
	def on_query_context(self, view, key, operator, operand, match_all):

		global TabrVariables

		if key == 'Tabr_tab' and TabrVariables['TabrActive'] == True:
			return True

class TabrGotoNextCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		global TabrVariables

		TabrVariables['TabrCurrentSelection'] += 1

		offset = 0
		for x in range(0, TabrVariables['TabrCurrentSelection']):
			offset += TabrVariables['TabrSelections'][x]['difference']

		if TabrVariables['TabrCurrentSelection'] < len(TabrVariables['TabrSelections']):
			self.view.sel().clear()
			self.view.sel().add( sublime.Region( TabrVariables['TabrSelections'][TabrVariables['TabrCurrentSelection']]['end'] + offset ) )
			
			# Reset View Size
			TabrVariables['viewSize'] = self.view.size()
			
			# Last Selection
			if (TabrVariables['TabrCurrentSelection'] + 1) == len(TabrVariables['TabrSelections']):
				TabrVariables['TabrActive'] = False
				TabrVariables['TabrSelections'] = []
				TabrVariables['TabrCurrentSelection'] = 0
				TabrVariables['viewSize'] = 0

class TabrCountCommand(sublime_plugin.EventListener):
	def on_modified(self, view):

		global TabrVariables

		if (len(TabrVariables['TabrSelections']) > 0):
			TabrVariables['TabrSelections'][TabrVariables['TabrCurrentSelection']]['difference'] = view.size() - TabrVariables['viewSize']
			TabrVariables['TabrSelections'][TabrVariables['TabrCurrentSelection']]['end'] = TabrVariables['TabrSelections'][TabrVariables['TabrCurrentSelection']]['start'] + TabrVariables['TabrSelections'][TabrVariables['TabrCurrentSelection']]['difference']