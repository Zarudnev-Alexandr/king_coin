function copyTextToClipboard(text: string) {
  if (!navigator.clipboard) {
    // Clipboard API не поддерживается, используем fallback
    const textArea = document.createElement("textarea");
    textArea.value = text;

    // Избегаем прокрутки на странице
    textArea.style.position = "fixed";
    textArea.style.top = "0";
    textArea.style.left = "0";

    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
      const successful = document.execCommand('copy');
      const msg = successful ? 'успешно' : 'неуспешно';
      console.log('Копирование текста ' + msg);
    } catch (err) {
      console.error('Ошибка при копировании текста', err);
    }

    document.body.removeChild(textArea);
    return;
  }
  navigator.clipboard.writeText(text).then(() => {
    console.log('Текст успешно скопирован в буфер обмена');
  }).catch((err) => {
    console.error('Ошибка при копировании текста в буфер обмена', err);
  });
}

export {
  copyTextToClipboard,
}
