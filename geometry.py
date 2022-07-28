def on_segment(p, q, r):
    pass


def orientation(p, q, r):
    coef = (q[1] - p[1])*(r[0] - q[0]) - (r[1] - q[1])*(q[0] - p[0])

    if coef < 0:
        # ccw
        return -1
    elif coef > 0:
        # cw
        return 1
    else:
        # collinear lines
        return 0


def intersect(p1, p2, w1, w2):
    conditions = (
        orientation(p1, p2, w1) != orientation(p1, p2, w2),
        orientation(w1, w2, p1) != orientation(w1, w2, p2),
    )
    return all(conditions)


if __name__ == "__main__":
    assert intersect((-150, 0), (150, 0), (0, -150), (0, 150)) == True
