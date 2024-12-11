from dataclasses import dataclass

from sortedcontainers import SortedKeyList


@dataclass(slots=True)
class Chunk:
    start: int
    length: int
    fileid: int = -1
    prev: "Chunk" = None
    next: "Chunk" = None

    def __repr__(self):
        return f"Chunk(start={self.start}, length={self.length}, fileid={self.fileid})"

    def append_to(self, prev):
        self.prev = prev
        if prev:
            prev.next = self
        return self

    def split(self, blocks: int, fileid=-1):
        """
        Split off a number of blocks from the start of this chunk and make them
        a new chunk with the specified fileid, inserted before self into the chain
        :return: the chunk that now starts at the same location as the previous start
        of self.  This may _be_ self, if blocks == self.length, but otherwise it will
        be a new chunk whose next is the current self truncated at the left.

        Before::

            prev--][-----self------][--next

        After::

            prev--][--new--][-self-][--next

        """
        assert blocks <= self.length, f"Attempted to split off {blocks} many blocks from chunk {self}"

        if blocks == self.length:
            # Special case, just re-label this block
            self.fileid = fileid
            return self

        # Create a new smaller chunk that will replace self in the chain
        new_chunk = Chunk(self.start, blocks, fileid, self.prev, self)
        # Connect the links - our _current_ prev's next is the new chunk, then our
        # _new_ prev becomes the new chunk
        self.prev.next = new_chunk
        self.prev = new_chunk

        # Adjust self length to allow for the new chunk
        self.length -= blocks
        self.start += blocks

        return new_chunk


def load_data() -> tuple[Chunk, Chunk]:
    with open("input", "r") as f:
        diskmap = f.read().strip()

    head = None
    cur = None
    start = 0
    for i, ch in enumerate(diskmap):
        chunklen = int(ch)
        if chunklen > 0:
            cur = Chunk(start, chunklen, i // 2 if i % 2 == 0 else -1).append_to(cur)
            start += chunklen
            if not head:
                head = cur

    return head, cur


def print_chain(head):
    print("--------")
    while True:
        print(head)
        head = head.next
        if head is None: break

def checksum(head: Chunk) -> int:
    checksum = 0
    while head is not None:
        if head.fileid >= 0:
            # The checksum of a chunk for file ID f starting at position P with length L
            # is equal to
            #
            # f * (P + P+1 + P+2 + ... + P+L-1)
            # = f * ((P-1)+1 + (P-1)+2 + ... + (P-1)+L)
            # = f * (L * (P-1) + (1 + 2 + ... + L))
            # = f * (L * (P-1) + (L * (L+1) / 2))  [standard formula for first L positive integers]
            #
            # which could be simplified further to f * L * (P-1 + (L+1)/2) but (L(L+1)/2) is
            # always an integer, (L+1)/2 on its own might not be.
            checksum += head.fileid * ((head.length * (head.start - 1)) + ((head.length * (head.length + 1)) // 2))
        head = head.next

    return checksum


def defragment():
    orig_head, tail = load_data()

    head = orig_head

    # Find the first gap
    while head.fileid >= 0:
        head = head.next

    # Find the last data chunk
    while tail.fileid < 0:
        tail = tail.prev


    while head is not tail:
        # move as many blocks as possible from the tail file into the head gap
        head = head.split(min(head.length, tail.length), tail.fileid)
        # shorten the tail chunk to compensate
        tail.length -= head.length

        # if the tail chunk is now empty, discard it and skip over any trailing gaps
        # to find the next tail file
        while head is not tail and (tail.length == 0 or tail.fileid < 0):
            tail = tail.prev
            tail.next = None

        # Find the next head gap
        while head is not tail and head.fileid >= 0:
            head = head.next

    # We've met in the middle so list is fully defragmented

    print(f"Disk checksum - packing all spaces: {checksum(orig_head)}")


def gap_key(gap: Chunk):
    return gap.start


def move_files():
    orig_head, tail = load_data()

    head = orig_head
    files: list[Chunk] = []
    gaps = SortedKeyList(key=gap_key)
    while head:
        if head.fileid >= 0:
            files.append(head)
        else:
            gaps.add(head)
        head = head.next

    for file in reversed(files):
        gap = None
        for i, g in enumerate(gaps):
            if g.start > file.start:
                # this gap is beyond the file's current location
                break
            if g.length >= file.length:
                # this gap is long enough to fit this file
                gap = g
                gaps.pop(i)
                break

        if gap:
            gap_len = gap.length
            new_file = gap.split(file.length, file.fileid)
            if file.length < gap_len:
                # There will still be some gap after this file, and it can't
                # be adjacent to any other gap
                trailing_gap = new_file.next
                gaps.add(trailing_gap)
            
            new_gap = file
            # file is now a gap, amalgamate it with any adjacent gaps
            new_gap.fileid = -1
            nxt = new_gap.next
            while new_gap.prev and new_gap.prev.fileid == -1:
                gaps.remove(new_gap.prev)
                l = new_gap.length
                new_gap = new_gap.prev
                new_gap.length += l
                new_gap.next = nxt
                
            while new_gap.next and new_gap.next.fileid == -1:
                gaps.remove(new_gap.next)
                new_gap.length += new_gap.next.length
                new_gap.next = new_gap.next.next
                if new_gap.next:
                    new_gap.next.prev = new_gap

            if new_gap.next:
                # There is still a file after this new gap, so add it back as a
                # valid gap to be filled
                gaps.add(new_gap)
            else:
                # This gap is at the end of the disk, so discard it
                if new_gap.prev:
                    new_gap.prev.next = None

    # all files processed, calculate the checksum
    print(f"Disk checksum - moving whole files: {checksum(files[0])}")


if __name__ == "__main__":
    defragment()
    move_files()