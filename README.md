vim-yo-spell
============

Плагин для [ёфикатора Евгения Миньковского][yo]

## Установка

```bash
echo 'Bundle "z2v/vim-yo-spell"' >> .vimrc
```

## Настройка

```vim
let g:vim_yo_spell_dict = $HOME . '/.vim/bundle/vim-yo-spell/yo.txt'
nnoremap <Leader>yo :pyf ~/.vim/bundle/vim-yo-spell/yo.py<CR>
```

[yo]: http://python.anabar.ru/yo.htm
