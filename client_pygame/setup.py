# run: python setup build in cmd
import cx_Freeze

executables = [cx_Freeze.Executable("client.py")]

cx_Freeze.setup(
    name="map-task",
    options={"build_exe": {"packages": ["pygame"],
                           "include_files": ["map1.png"]}},
    executables=executables
)
