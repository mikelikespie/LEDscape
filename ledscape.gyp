{  
  'targets': [
    {
      'target_name': 'pasm',
      'type': 'executable',
      'sources': [
        'am335x/pasm/pasm.c',
        'am335x/pasm/pasm.h',
        'am335x/pasm/pasmdbg.h',
        'am335x/pasm/pasmdot.c',
        'am335x/pasm/pasmexp.c',
        'am335x/pasm/pasmmacro.c',
        'am335x/pasm/pasmop.c',
        'am335x/pasm/pasmpp.c',
        'am335x/pasm/pasmstruct.c',
        'am335x/pasm/pru_ins.h',
      ],
    },
    {
      'target_name': 'pruss',
      'type': 'static_library',
      'include_dirs': [
        "am335x/app_loader/include",
      ],
      'link_settings': {
        'libraries': [
          '-lpthread'
        ]
      },
      'direct_dependent_settings': {
        'include_dirs': [
          "am335x/app_loader/include",
        ],
      },
      'sources': [
        'am335x/app_loader/include/pruss_intc_mapping.h',
        'am335x/app_loader/include/prussdrv.h',
        'am335x/app_loader/interface/__prussdrv.h',
        'am335x/app_loader/interface/prussdrv.c',
      ],
    },
    {
      'target_name': 'ledscape',
      'type': 'static_library',
      'dependencies': [
        'pruss',
        'pasm',
      ],
      'include_dirs': [
        '.',
        '<(INTERMEDIATE_DIR)',
      ],
      'direct_dependent_settings': {
        'include_dirs': [
          '.',
        ],
      },
      'sources': [
        'ledscape.c',
        'ledscape.h',
        'pru.c',
        'pru.h',
        'ws281x.p',
        '<(INTERMEDIATE_DIR)/ws281x.pi',
        '<(INTERMEDIATE_DIR)/ws281x_bin.h',
      ],
      'rules': [
        {
          'rule_name': 'preprocess PRU image',
          'extension': '.p',
          'outputs': [
            '<(INTERMEDIATE_DIR)/<(RULE_INPUT_ROOT).pi',
          ],
          'action': [
            '<@(preprocess_asm)',
            '<(RULE_INPUT_PATH)',
            '<@(_outputs)',
          ],
        },
        {
          'rule_name': 'process PRU image',
          'extension': '.pi',
          'outputs': [
            '<(INTERMEDIATE_DIR)/<(RULE_INPUT_ROOT)_bin.h',
          ],
          'action': [
            '<(pasm)',
            '-V3',
            '-c',
            '-C<(RULE_INPUT_ROOT)_PRUcode',
            '<(RULE_INPUT_PATH)',
            '<(INTERMEDIATE_DIR)/<(RULE_INPUT_ROOT)',
          ],
        },
      ],
    },
    {
      'target_name': 'rgb-test',
      'type': 'executable',
      'dependencies': [
        'ledscape',
      ],
      'link_settings': {
        'libraries': [
          '-lm'
        ]
      },
      'sources': [
        'rgb-test.c',
      ],
    },
  ],
  'target_defaults': {
    'cflags': [
      '-std=c99',
      '-O3',
    ],
  },
  'variables': {
    'pasm': '<(PRODUCT_DIR)/<(EXECUTABLE_PREFIX)pasm<(EXECUTABLE_SUFFIX)',
    'preprocess_asm': ['python', 'preprocess_asm.py'],
  },
  'make_global_settings': [
    ['CC','/usr/bin/clang'],
    ['CXX','/usr/bin/clang++'],
    ['LINK','/usr/bin/clang++'],
  ],
}



