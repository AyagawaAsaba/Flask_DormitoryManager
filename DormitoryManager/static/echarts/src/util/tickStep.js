define(function (require) {

    var numberUtil = require('./number');

    /**
     * Computing the length of step
     * @see  https://github.com/d3/d3-array/blob/master/src/ticks.js
     * @param {number} start
     * @param {number} stop
     * @param {number} count
     */
    return function (start, stop, count) {

        var step0 = Math.abs(stop - start) / count;
        var precision = numberUtil.quantityExponent(step0);

        var step1 = Math.pow(10, precision);
        var error = step0 / step1;

        if (error >= Math.sqrt(50)) {
            step1 *= 10;
        } else if (error >= Math.sqrt(10)) {
            step1 *= 5;
        } else if (error >= Math.sqrt(2)) {
            step1 *= 2;
        }

        var toFixedPrecision = precision < 0 ? -precision : 0;
        var resultStep = +(
            (stop >= start ? step1 : -step1).toFixed(toFixedPrecision)
        );

        return {
            step: resultStep,
            toFixedPrecision: toFixedPrecision
        };
    };

});
