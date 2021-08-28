export const getAllCells = () => {
    const cells = []
    for (let x=0; x<=4; x++) {
        for (let z=0; z<=6; z++) {
            if (
                z == 1 && [1, 3].includes(x)
            || z == 2 && [1, 2, 3].includes(x)
            || z == 3 && [1, 2, 3].includes(x)) {
                continue
            }
            cells.push([x, 3, z])
        }
    }
    return cells;
}