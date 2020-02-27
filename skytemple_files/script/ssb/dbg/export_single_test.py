"""Testing script for testing a SSB file."""
#  Copyright 2020 Parakoopa
#
#  This file is part of SkyTemple.
#
#  SkyTemple is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SkyTemple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.
import os

from ndspy.rom import NintendoDSRom

from skytemple_files.common.script_util import load_script_files, SCRIPT_DIR
from skytemple_files.common.util import get_rom_folder, get_files_from_rom_with_extension
from skytemple_files.script.ssb.handler import SsbHandler

output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
os.makedirs(output_dir, exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

script_info = load_script_files(get_rom_folder(rom, SCRIPT_DIR))


for file_name in get_files_from_rom_with_extension(rom, 'ssb'):
    # Files that don't work right now:
    print(file_name)

    out_file_name = os.path.join(output_dir, file_name.replace('/', '_') + '.txt')

    bin_before = rom.getFileByName(file_name)
    ssb = SsbHandler.deserialize(bin_before)

    with open(out_file_name, 'w') as f:
        lines = []
        lines.append(str(ssb.header))
        lines.append(f"number_of_routines: {len(ssb.routine_info)}")
        lines.append(f"constants: {ssb.constants}")
        lines.append(f"strings: {ssb.strings}")
        lines.append(str(ssb.routine_info))
        for ops in ssb.routine_ops:
            lines.append(">>> Routine:")
            op_cursor = 0
            for op in ops:
                lines.append(f"{op_cursor:10}: {op}")
                op_cursor += 2 + len(op.params) * 2
        f.writelines([l + '\n' for l in lines])