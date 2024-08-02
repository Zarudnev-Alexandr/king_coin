const setScreenHeight = {
  beforeMount(el: HTMLElement) {
    const updateHeight = () => {
      el.style.height = `${window.innerHeight}px`;
    };

    updateHeight();
    window.addEventListener('resize', updateHeight);

    // Сохраняем ссылку на функцию для удаления слушателя в элементе
    (el as any)._onResize = updateHeight;
  },
  unmounted(el: HTMLElement) {
    window.removeEventListener('resize', (el as any)._onResize);
  },
};

export default setScreenHeight;
