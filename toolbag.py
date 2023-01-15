import proto as proto
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
        c_id = p.selected["Chunk"]
        chunks = theatre_.the_stage.chunks
        this_t = p.selected["This Tile"]
        that_t = p.selected["That Tile"]
        this_id = str(this_t[0])+','+str(this_t[1])
        that_id = str(that_t[0])+','+str(that_t[1])
        this_tile = chunks[c_id].tiles[this_id]
        this_t_pos = this_tile.instance.getPos()
        if player:
            txt = '_______________\nDebug - Map Info:\n'
            txt += ' - This Chunk: '+c_id+'\n'
            txt += ' - This Tile: Map ('+this_id+')'
            txt += ' - Vector ('
            txt += str(this_t_pos[0])+','+str(this_t_pos[1])+')\n'
            txt += ' - That Tile: ('+that_id+') \n'
            txt += 'Draw pointer at: '
            txt += '('+str(p.draw_at[0])+','+str(p.draw_at[1])+')\n'
            t_count = 0
            txt += '# of tiles in:\n'
            for i in chunks:
                txt += '    "'+chunks[i].chunk_id+'": '+str(len(chunks[i].tiles))+'\n'
                t_count += len(chunks[i].tiles)
            txt += '       Total # of tiles: '+str(t_count)+'\n'
            return txt
