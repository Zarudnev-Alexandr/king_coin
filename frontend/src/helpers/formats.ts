function formatNumber(num: number): string {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1).replace(/\.0$/, '') + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1).replace(/\.0$/, '') + 'K';
    } else {
        return num.toString();
    }
}

function formatNumberWithSpaces(num: number): string {
    const numFloor = Math.floor(num);
    return numFloor.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}

export {
    formatNumber,
    formatNumberWithSpaces,
}