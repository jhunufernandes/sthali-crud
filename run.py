from sthali_crud import SthaliCRUD, AppSpecification


spec = {
    'resources': [
        {
            'db_engine': 'tinydb',
            'name': 'cats',
            'fields': [
                {
                    'name': 'name',
                    'type': str,
                },
                {
                    'name': 'age',
                    'type': int,
                }
            ]
        },
        {
            'db_engine': 'tinydb',
            'name': 'dogs',
            'fields': [
                {
                    'name': 'name',
                    'type': str,
                },
                {
                    'name': 'fur',
                    'type': bool,
                }
            ]
        }

    ]
}


sthalicrud = SthaliCRUD(AppSpecification(**spec)).app
