#! /usr/bin/env python

from aoc.utils import load_input


def get_layers(img_data, w, h):
    layer_size = w * h

    return [[int(c) for c in img_data[i : i + layer_size]] for i in range(0, len(img_data), layer_size)]


def merge_layers(layers):
    merged = []

    for i in range(len(layers[0])):
        for l in layers:
            if l[i] in (0, 1):
                merged.append(l[i])
                break
        else:
            merged.append(-1)

    return merged


def render_image(img_data, w, h):
    for y in range(h):
        for x in range(w):
            px = img_data[x + y * w]
            print("X" if px == 1 else " ", end="")

        print()


def main():
    img_data = load_input("d08.txt")
    w, h = 25, 6

    nb0 = 2 ** 64
    layers = get_layers(img_data, 25, 6)
    p1 = 0
    for l in layers:
        c = l.count(0)
        if c < nb0:
            p1 = l.count(1) * l.count(2)
            nb0 = c

    print(f"Part 1: {p1}")

    final_img = merge_layers(layers)
    print("Part 2:")
    print(render_image(final_img, w, h))


if __name__ == "__main__":
    from time import time as ts

    _t = ts()
    main()
    _t = ts() - _t

    print(f"Took {_t:.3f}s")
