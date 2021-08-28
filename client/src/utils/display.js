export const formattedValue = (value) => {
    if (value === false) return 'False';
    if (value === true) return 'True';
    if (value === null || value === undefined) return 'Undefined';
    return value;
}