import protorefactor as proto
from uiwin import MapTab


class Director:
    @staticmethod
    # ! Unfinished !
    def style_this(colors=proto.default_ui_colors, aoa_win=None):
        # Pass in player.ui_colors and the AoaWindow() to style.
        if aoa_win:
            c = colors['Root BG']
            aoa_win.root['bg'] = c
            c = colors['ChatSection - BG']
            aoa_win.chat_output['bg'] = c
            c = colors['TNotebook - BG']
            aoa_win.ttk_style.configure('TNotebook', background=c)
            aoa_win.ttk_style.configure('TNotebook', tabmargins=[0, 0, 0, 0])
            c = colors['TNotebook.Tab - BG']
            aoa_win.ttk_style.configure('TNotebook.Tab', background=c)
            c = colors['TNotebook.Tab - Selected BG']
            aoa_win.ttk_style.map('TNotebook.Tab', background=[('selected', c)])
        else:
            print('No window')


class GetInfo:
    @staticmethod
    def draw_map_info(player=None, theatre_=None):
        p = theatre_.pointer
        if player:
            txt = '_______________\nDebug - Map Info:\n'
            txt += ' - This Chunk: '
            txt += p.selected['Chunk']+'\n'
            txt += ' - This Tile: ('
            txt += str(p.selected['This Tile'][0])+','
            txt += str(p.selected['This Tile'][1])+') \n'
            txt += ' - That Tile: ('
            txt += str(p.selected['That Tile'][0])+','
            txt += str(p.selected['That Tile'][1])+') \n'
            t_count = 0
            c = theatre_.the_stage.chunks
            txt += '# of tiles in:\n'
            for i in c:
                txt += '    "'+c[i].chunk_id+'": '+str(len(c[i].tiles))+'\n'
                t_count += len(c[i].tiles)
            txt += '       Total # of tiles: '+str(t_count)+'\n'
            return txt
