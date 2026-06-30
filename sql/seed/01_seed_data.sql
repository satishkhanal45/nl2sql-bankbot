-- SEED DATA: entity
INSERT INTO entity (entity_name, fact) VALUES
    ('bank', 'central_bank'),
    ('bank', 'home_loan'),
    ('bank', 'main_branch'),
    ('bank', 'saving_account'),
    ('bank', 'fixed_deposit'),
    ('bank', 'sub_branch'),
    ('bank', 'personal_loan'),
    ('bank', 'vehicle_loan')
ON CONFLICT (entity_name, fact) DO NOTHING;


-- SEED DATA: attribute
INSERT INTO attribute (label) VALUES
    ('address'),
    ('email'),
    ('phone'),
    ('interest_rate'),
    ('loan_amount'),
    ('website'),
    ('manager'),
    ('minimum_balance'),
    ('maximum_balance'),
    ('tenure'),
    ('processing_fee'),
    ('collateral'),
    ('loan_type')
ON CONFLICT (label) DO NOTHING;



-- SEED DATA: entity_value
INSERT INTO entity_value (entity_id, attribute_id, path_name, value, type) VALUES

    -- central_bank (entity_id=1)
    (1, 1, 'bank.central_bank.address',  'Baluwatar, Kathmandu',  'string'),
    (1, 2, 'bank.central_bank.email',    'info@nrb.org.np',       'string'),
    (1, 3, 'bank.central_bank.phone',    '01-4419804',            'string'),
    (1, 6, 'bank.central_bank.website',  'www.nrb.org.np',        'string'),
    (1, 7, 'bank.central_bank.manager',  'Maha Prasad Adhikari',  'string'),

    -- home_loan (entity_id=2)
    (2, 4,  'bank.home_loan.interest_rate',  '8.5',                   'numeric'),
    (2, 5,  'bank.home_loan.loan_amount',    '5000000',               'numeric'),
    (2, 10, 'bank.home_loan.tenure',         '20',                    'numeric'),
    (2, 1,  'bank.home_loan.address',        'Baneshwor, Kathmandu',  'string'),
    (2, 11, 'bank.home_loan.processing_fee', '0.5',                   'numeric'),
    (2, 12, 'bank.home_loan.collateral',     'Property',              'string'),

    -- main_branch (entity_id=3)
    (3, 1, 'bank.main_branch.address',  'New Baneshwor, Kathmandu',  'string'),
    (3, 2, 'bank.main_branch.email',    'branch@bank.com.np',        'string'),
    (3, 3, 'bank.main_branch.phone',    '01-4780040',                'string'),
    (3, 7, 'bank.main_branch.manager',  'Ram Prasad Sharma',         'string'),
    (3, 6, 'bank.main_branch.website',  'www.bank.com.np',           'string'),

    -- saving_account (entity_id=4)
    (4, 4, 'bank.saving_account.interest_rate',   '5.5',    'numeric'),
    (4, 8, 'bank.saving_account.minimum_balance',  '1000',  'numeric'),
    (4, 9, 'bank.saving_account.maximum_balance',  '500000','numeric'),

    -- fixed_deposit (entity_id=5)
    (5, 4,  'bank.fixed_deposit.interest_rate',   '10.5',  'numeric'),
    (5, 8,  'bank.fixed_deposit.minimum_balance',  '10000', 'numeric'),
    (5, 10, 'bank.fixed_deposit.tenure',           '1',     'numeric'),

    -- sub_branch (entity_id=6)
    (6, 1, 'bank.sub_branch.address',  'Lalitpur, Patan',       'string'),
    (6, 2, 'bank.sub_branch.email',    'subbranch@bank.com.np', 'string'),
    (6, 3, 'bank.sub_branch.phone',    '01-5432100',            'string'),
    (6, 7, 'bank.sub_branch.manager',  'Sita Thapa',            'string'),

    -- personal_loan (entity_id=7)
    (7, 4,  'bank.personal_loan.interest_rate',  '12.5',    'numeric'),
    (7, 5,  'bank.personal_loan.loan_amount',     '1000000', 'numeric'),
    (7, 10, 'bank.personal_loan.tenure',          '5',       'numeric'),
    (7, 11, 'bank.personal_loan.processing_fee',  '1.0',     'numeric'),
    (7, 12, 'bank.personal_loan.collateral',      'None',    'string'),
    (7, 13, 'bank.personal_loan.loan_type',       'Unsecured','string'),

    -- vehicle_loan (entity_id=8)
    (8, 4,  'bank.vehicle_loan.interest_rate',  '11.0',    'numeric'),
    (8, 5,  'bank.vehicle_loan.loan_amount',     '2000000', 'numeric'),
    (8, 10, 'bank.vehicle_loan.tenure',          '7',       'numeric'),
    (8, 11, 'bank.vehicle_loan.processing_fee',  '0.75',    'numeric'),
    (8, 12, 'bank.vehicle_loan.collateral',      'Vehicle', 'string'),
    (8, 13, 'bank.vehicle_loan.loan_type',       'Secured', 'string')

ON CONFLICT (entity_id, attribute_id) DO NOTHING;