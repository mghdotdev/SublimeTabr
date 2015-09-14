import sublime
import sublime_plugin

TabberSelections = []
TabberSelectionCounter = 0;

class TabberCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		TabberSelections = []
		selections = self.view.sel()
		
		for region in selections:

			TabberSelections.append([region.begin(), region.end()])
			self.view.replace(edit, region, '')

		self.view.sel().clear()
		self.view.sel().add(sublime.Region(TabberSelections[0][0]))

class TabberTabHandler(sublime_plugin.EventListener):
	def on_query_context(self, view, key, operator, operand, match_all):

		# if key != 'tabber':
		# 	return None
		# else:
		# 	return True

		# print(key)

class TabberGoToNextCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		print('Hi There!')