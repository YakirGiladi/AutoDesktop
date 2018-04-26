def insert_to_actions_list(text="", openfile = False, cond = True):

            print(self.line_start)
            text_actions_list.config(state=NORMAL)
            if self.line_start == 0:
                self.line_start = INSERT
            
            if openfile:
                text_actions_list.insert(INSERT, '{}'.format(text))

            elif last_lineindex() == "1.0" and text == "": # Start of list
                # print("0")
                text_actions_list.insert(INSERT, '{}:'.format(condition()))

            elif self.line_end == END: # End of list
                # print("END")
                text_actions_list.insert(INSERT, '{}\n{}:'.format(text,condition()))
            else:
                if cond:
                    # print("1")
                    text_actions_list.insert(self.line_start, '{}\n{}:'.format(text,condition()))
                else:
                    # print("2")
                    text_actions_list.insert(self.line_start, '{}'.format(text))

            text_actions_list.config(state=DISABLED)
            text_actions_list.tag_remove("highlight", 1.0, "end")