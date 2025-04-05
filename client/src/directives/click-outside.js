export default {
    mounted(el, binding) {
        el.clickOutsideEvent = function (event) {
            if (!(el == event.target || el.contains(event.target))) {
                binding.value(event);
            }
        };
        document.addEventListener('click', el.clickOutsideEvent);
    },
    
    beforeUnmount(el) {
        document.removeEventListener('click', el.clickOutsideEvent);
    }
};