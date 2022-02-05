
import wordle_filter as wf
import dearpygui.dearpygui as dpg

class MainWindow():

    def __init__(self):
        words = wf.load(wf.wordfile)
        words_alt = words.copy()
        letters = wf.load(wf.letterfile)
        possible_word_count = len(words)

        dpg.create_context()
        dpg.create_viewport(title="wordle_filter",width=500,height=800)
        dpg.setup_dearpygui()

        with dpg.theme() as red_text_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 0, 0])

        with dpg.theme() as yellow_text_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 211, 67])

        with dpg.theme() as green_text_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Text, [121, 184, 81])

        with dpg.theme() as reset_button_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Text, [0, 0, 0])
                dpg.add_theme_color(dpg.mvThemeCol_Button, [200, 0, 0])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [255, 0, 0])

        with dpg.window(label="Example Window",tag="Primary Window"):

            with dpg.group(horizontal=True) as row:
                reset_button = dpg.add_button(label="Reset", callback=self.reset, tag='')
                dpg.add_text('<-- this button will clear all inputs')
                dpg.bind_item_theme(reset_button, reset_button_theme)

            x = dpg.add_text('excluded - words with these letters will be excluded')
            y = dpg.add_input_text(tag='##excluded',width=450,label="", default_value="", callback=self.refresh)

            dpg.bind_item_theme(x, red_text_theme)
            dpg.bind_item_theme(y, red_text_theme)

            dpg.add_text('----------------------------------------------------')

            x = dpg.add_text('included - words with these letters will be included')
            y = dpg.add_input_text(tag='##included',width=450,label="", default_value="", callback=self.refresh)

            dpg.bind_item_theme(x, yellow_text_theme)
            dpg.bind_item_theme(y, yellow_text_theme)

            dpg.add_text('----------------------------------------------------')

            x = dpg.add_text('known_positions - letters where we know the exact position')
            dpg.bind_item_theme(x, green_text_theme)
            x = dpg.add_text('\t. = unknown')
            dpg.bind_item_theme(x, green_text_theme)

            x = dpg.add_input_text(tag='##known_positions',width=450,label="", default_value=".....", callback=self.refresh)
            dpg.bind_item_theme(x, green_text_theme)

            # with dpg.group(horizontal=True) as row:
            #     v = dpg.add_input_text(tag='##1',width=25,label="", default_value=".", callback=self.refresh)
            #     w = dpg.add_input_text(tag='##2',width=25,label="", default_value=".", callback=self.refresh)
            #     x = dpg.add_input_text(tag='##3',width=25,label="", default_value=".", callback=self.refresh)
            #     y = dpg.add_input_text(tag='##4',width=25,label="", default_value=".", callback=self.refresh)
            #     z = dpg.add_input_text(tag='##5',width=25,label="", default_value=".", callback=self.refresh)

            #     dpg.bind_item_theme(v, green_text_theme)
            #     dpg.bind_item_theme(w, green_text_theme)
            #     dpg.bind_item_theme(x, green_text_theme)
            #     dpg.bind_item_theme(y, green_text_theme)
            #     dpg.bind_item_theme(z, green_text_theme)

            dpg.add_text('----------------------------------------------------')
            dpg.add_text('{} possible words'.format(possible_word_count),tag='##pw_count')
            dpg.add_input_text(tag='##possible_words',width=450,height=200,multiline=True,label="", default_value="")
            dpg.add_text('words to try')
            dpg.add_input_text(tag='##words_to_try',width=450,height=200,multiline=True,label="", default_value="")

        dpg.set_primary_window("Primary Window", True)
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def reset(self,sender):
        dpg.set_value('##known_positions','.....')
        dpg.set_value('##excluded','')
        dpg.set_value('##included','')


    def refresh(self,sender):
        # dpg.set_value('##1',('.' + dpg.get_value('##1'))[-1].upper())
        # dpg.set_value('##2',('.' + dpg.get_value('##2'))[-1].upper())
        # dpg.set_value('##3',('.' + dpg.get_value('##3'))[-1].upper())
        # dpg.set_value('##4',('.' + dpg.get_value('##4'))[-1].upper())
        # dpg.set_value('##5',('.' + dpg.get_value('##5'))[-1].upper())

        dpg.set_value('##known_positions',('.....' + dpg.get_value('##known_positions'))[-5:].upper())

        excluded = wf.upperize(dpg.get_value('##excluded'))
        included = wf.upperize(dpg.get_value('##included'))
        known_positions = dpg.get_value('##known_positions')
        words = wf.load(wf.wordfile)
        words_alt = words.copy()
        letters = wf.load(wf.letterfile)
        
        words = wf.filter_excluded(words,excluded)
        words = wf.filter_included(words,included)
        words = wf.filter_kp(words,known_positions)
        possible_word_count = len(words)
        dpg.set_value('##pw_count','{} possible words'.format(possible_word_count))
        dpg.set_value('##possible_words','\n'.join(words))

        testable_letters = letters
        testable_letters = wf.filter_excluded(testable_letters,excluded)
        testable_letters = wf.filter_excluded(testable_letters,included)
        testable_letters = wf.filter_excluded(testable_letters,known_positions)
        testable_letters = ''.join(testable_letters)
        words_to_try = wf.filter_wtt(words_alt,testable_letters,10)

        wtt = ''
        for i in words_to_try:
            wtt = wtt + i['word'] + ' - ' + str(i['count']) + '\n'

        dpg.set_value('##words_to_try',wtt)


if __name__ == "__main__":
    MW = MainWindow()



