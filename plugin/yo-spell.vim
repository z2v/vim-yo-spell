if !has('python')
    echo "Error: Required vim compiled with +python"
    finish
endif

if exists('vim_yo_spell_module')
        finish
endif

let vim_yo_spell_module = 1

let g:vim_yo_spell_path = expand('<sfile>:p:h')
let g:vim_yo_spell_dict = vim_yo_spell_path . '/' . 'yo.txt'

python << EOF
import sys, vim
sys.path.append(vim.eval("g:vim_yo_spell_path"))
EOF


function RunYoSpell()

    python << EOF
import yo
yo.main()
EOF

endfunction

nnoremap <Leader>yo :call RunYoSpell()<CR>
