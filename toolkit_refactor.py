

class InputHandler:
    @staticmethod
    def get_input(aoa_window=None):
        aw = aoa_window
        keys = aw.the_player.data.key_map
        if aw:
            print('get input')


class MobHandler:
    @staticmethod
    def mob_collection(aoa_window=None):
        p = aoa_window.ThePlayer.data
        m = aoa_window.TheMap.data
        mob_list = {}
        mob_list.update(p.pc_party)
        mob_list.update(m.non_player_characters)
        mob_list.update(m.enemies)
        return mob_list

    @staticmethod
    def motivate_mobs(aoa_window=None):
        c = MobHandler.mob_collection(aoa_window)
        for i in c:
            if c[i].is_moving:
                print('move character towards target')

