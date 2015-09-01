import sublime
import sublime_plugin

class TabberCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		# Set Variable `selections` to current selection array
		selections = self.view.sel()

		# Define `placeholder` variable and loop through `selections`
		placeholder = 0;
		for region in selections:

			# Set `placeholder` to increment | if last iteration... set `placeholder` to 0
			placeholder += 1
			if placeholder == len(selections):
				placeholder = 0

			# Run Command `replace` on `region`
			self.view.replace(edit, region, '$=' + str(placeholder))




#### TEST ZONE ####
# self.view.run_command('insert_snippet', {"contents": "$1$0"})
