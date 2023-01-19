
class DeBug:
    @staticmethod
    def draw_map_info(player=None, theatre_=None):
        p = theatre_.pointer
        c_id = p.selected["Chunk"]
        chunks = theatre_.the_stage.chunks
        this_t = p.selected["This Tile"]
        that_t = p.selected["That Tile"]
        this_id = str(this_t[0])+','+str(this_t[1])
        this_tile = chunks[c_id].tiles[this_id]
        this_t_pos = this_tile.instance.getPos()
        that_id = str(that_t[0])+','+str(that_t[1])
        if that_id in chunks[c_id].tiles:
            that_tile = chunks[c_id].tiles[that_id]
            that_t_pos = that_tile.instance.getPos()
        else:
            that_tile = None
            that_t_pos = None
        if player:
            txt = '_'*50+'\nDebug - Map Info:\n'
            txt += 'This Chunk: '+c_id+'\n'
            txt += ' - This Tile: Map ('+this_id+')'
            txt += ' - Vector ('
            txt += str(this_t_pos[0])+','+str(this_t_pos[1])+')\n'
            txt += ' - That Tile: '
            if that_tile:
                txt += 'Map ('+that_id+')'
                txt += ' - Vector ('
                txt += str(that_t_pos[0]) + ',' + str(that_t_pos[1]) + ')\n'
            else:
                txt += ' - No Tile - \n'
            txt += ' - Pointer: ('
            txt += '(' + str(p.map_loc[0]) + ',' + str(p.map_loc[1]) + ')\n'
            t_count = 0
            txt += '# of tiles in:\n'
            for i in chunks:
                txt += '    "'+chunks[i].chunk_id+'": '
                txt += str(len(chunks[i].tiles))+'\n'
                t_count += len(chunks[i].tiles)
            txt += '       Total # of tiles: '+str(t_count)+'\n'
            return txt

