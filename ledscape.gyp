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
      'target_name': 'app_loader',
      'type': 'static_library',
      'include_dirs': [
        "am335x/app_loader/include",
      ],
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
  ],
}


