from copy import deepcopy
from dataclasses import dataclass
import sys
from typing import Tuple, List
import enum


class BlockType(enum.Enum):
    NUMBER = 0
    SPACE = 1


@dataclass
class Block:
    id: int  # block with none id == space
    cardinality: int
    block_type: BlockType

    # property cardinality -> on setter set block type as SPACE
    def __repr__(self):
        return "-".join(
            [str(self.id), str(self.cardinality), str(self.block_type.name)]
        )


def parse_disk_structure(disk_structure: str) -> List[Block]:
    blocks = []
    number_block_id = 0
    for idx, cardinality in enumerate(disk_structure):
        if idx % 2 == 0:
            # number
            blocks.append(
                Block(
                    id=number_block_id,
                    cardinality=cardinality,
                    block_type=BlockType.NUMBER,
                ),
            )

            number_block_id += 1
        else:
            # space
            blocks.append(
                Block(id=None, cardinality=cardinality, block_type=BlockType.SPACE)
            )
    return blocks


def find_rightmost_block(
    blocks: List[Block], index: int, block_type: BlockType, fitting: bool
) -> int:
    min_size = blocks[index].cardinality if fitting else 1
    for i in range(len(blocks) - 1, index, -1):
        if blocks[i].block_type == block_type and blocks[i].cardinality >= min_size:
            return i
    return -1


def calculate_checksum(blocks: List[Block]) -> int:
    checksum = 0
    id = 0
    for i in range(len(blocks)):
        if blocks[i].block_type == BlockType.NUMBER:
            for _ in range(blocks[i].cardinality):
                checksum += id * blocks[i].id
                id += 1
        else:
            for _ in range(blocks[i].cardinality):
                id += 1
    return checksum


def defrag(blocks: List[Block]) -> int:
    # for each block space -> replace it with one or more blocks, starting from the rightmost ones
    i = 0
    while i < len(blocks):
        if blocks[i].block_type == BlockType.SPACE:
            # find rightmost block
            #   => if so, replace the space block with the number block and change the type to the number block
            #       to space block
            # check if cardinality < of space cardinality
            # restart and add a new number block instead of replacing it
            rightmost_index = find_rightmost_block(blocks, i, BlockType.NUMBER, False)
            if rightmost_index == -1:
                # no more number blocks on the right
                break
            number_block = blocks[rightmost_index]

            if number_block.cardinality > blocks[i].cardinality:
                blocks[i].block_type = BlockType.NUMBER
                number_block.cardinality -= blocks[i].cardinality
                blocks[i].id = number_block.id
            elif number_block.cardinality == blocks[i].cardinality:
                blocks[i].block_type = BlockType.NUMBER
                blocks[i].id = number_block.id
                number_block.cardinality = 0
                number_block.block_type = BlockType.SPACE
            else:
                blocks[i].cardinality -= number_block.cardinality
                blocks.insert(i, blocks.pop(rightmost_index))
            i += 1
        else:
            i += 1

    return calculate_checksum(blocks)


def defrag_whole_file_only(blocks: List[Block]) -> int:
    blocks = blocks[::-1]
    i = 0
    while i < len(blocks):
        if blocks[i].block_type == BlockType.NUMBER:
            rightmost_index = find_rightmost_block(blocks, i, BlockType.SPACE, True)
            if rightmost_index == -1:
                i += 1
            else:
                space_block = blocks[rightmost_index]
                if space_block.cardinality > blocks[i].cardinality:
                    space_block.cardinality -= blocks[i].cardinality
                    cardinality = blocks[i].cardinality
                    blocks.insert(rightmost_index, blocks.pop(i))
                    blocks.insert(i, Block(None, cardinality, BlockType.SPACE))
                elif space_block.cardinality == blocks[i].cardinality:
                    space_block.id = blocks[i].id
                    space_block.block_type = BlockType.NUMBER
                    blocks[i].block_type = BlockType.SPACE
                    i += 1
                else:
                    raise Exception("find_rightmost_block returned the wrong index")
        else:
            i += 1
    blocks = blocks[::-1]
    return calculate_checksum(blocks)


if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename) as f:
        disk_structure = map(int, f.readline().rstrip())
    blocks = parse_disk_structure(disk_structure)
    original_blocks = deepcopy(blocks)

    print(f"part 1: {defrag(blocks)}")
    print(f"part 2: {defrag_whole_file_only(original_blocks)}")
