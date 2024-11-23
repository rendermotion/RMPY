from RMPY.core import file_os
from builder.pipeline import environment



class Outputs(object):
    def __init__(self):
        pass
    @property
    def file_path(self):
        env = environment.Environment()
        file_path = env.data
        file_os.validate_path(file_path)
        # file_path = file_os.get_file_path()
        if not file_path:
            print('setting output to C:/RMPYData/')
            return 'C:/RMPYData/'
        else:
            print('setting output to {}'.format(file_path))
            return file_path

output = Outputs()

axis_order = 'xyz'

axis_order_index = ['xyz'.index(each) for each in axis_order]

default_reference_system_name = 'reference'

# file_path = file_os.get_file_path()

mirror_controls_axis = 'z'
mirror_controls = True


if __name__ == '__main__':
    pass
