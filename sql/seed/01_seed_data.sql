-- ============================================================
-- SEED DATA: entity (category-level grouping)
-- ============================================================
INSERT INTO entity (entity_name, fact) VALUES
    ('bank', 'branch'),
    ('bank', 'loan'),
    ('bank', 'card'),
    ('bank', 'atm'),
    ('bank', 'account'),
    ('bank', 'service'),
    ('bank', 'organization')
ON CONFLICT (entity_name, fact) DO NOTHING;


-- ============================================================
-- SEED DATA: attribute
-- ============================================================
INSERT INTO attribute (label) VALUES
    -- Branch attributes (id 1-12)
    ('address'),
    ('phone'),
    ('email'),
    ('website'),
    ('manager'),
    ('opening_hours'),
    ('branch_code'),
    ('province'),
    ('district'),
    ('city'),
    ('atm_available'),
    ('parking_available'),
    -- Loan attributes (id 13-22)
    ('interest_rate'),
    ('minimum_loan_amount'),
    ('maximum_loan_amount'),
    ('minimum_tenure'),
    ('maximum_tenure'),
    ('processing_fee'),
    ('collateral'),
    ('eligibility'),
    ('required_documents'),
    ('loan_type'),
    -- Account attributes (id 23-27)
    ('minimum_deposit'),
    ('maximum_deposit'),
    ('currency'),
    ('interest_calculation'),
    ('maturity_period'),
    -- Card attributes (id 28-38)
    ('annual_fee'),
    ('joining_fee'),
    ('cashback'),
    ('reward_points'),
    ('replacement_fee'),
    ('pin_generation'),
    ('cash_withdrawal_limit'),
    ('transaction_limit'),
    ('service_charge'),
    ('registration_requirement'),
    ('supported_platforms'),
    -- Common attributes (id 39-42)
    ('availability'),
    ('deposit_machine_available'),
    ('mini_statement'),
    ('balance_inquiry'),
    -- Organization attributes (id 43-50)
    ('toll_free_number'),
    ('support_hours'),
    ('grievance_email'),
    ('grievance_phone'),
    ('resolution_time'),
    ('swift_code'),
    ('established_year'),
    ('total_branches')
ON CONFLICT (label) DO NOTHING;


-- ============================================================
-- SEED DATA: entity_value
-- path_name = bank.<category>.<instance>.<attribute>
-- ============================================================
INSERT INTO entity_value (entity_id, attribute_id, path_name, value, type) VALUES
-- ── Category: branch (entity_id=1) ────────────────────────────────────
-- Instance: anamnagar
(1,  1,  'bank.branch.anamnagar.address',           'Anamnagar, Kathmandu, Bagmati Province',   'string'),
(1,  2,  'bank.branch.anamnagar.phone',             '01-4102030',                               'string'),
(1,  3,  'bank.branch.anamnagar.email',             'anamnagar@globalbank.com.np',              'string'),
(1,  4,  'bank.branch.anamnagar.website',           'www.globalbank.com.np',                    'string'),
(1,  5,  'bank.branch.anamnagar.manager',           'Ramesh Shrestha',                          'string'),
(1,  6,  'bank.branch.anamnagar.opening_hours',     'Sunday–Friday 10:00 AM – 5:00 PM',        'string'),
(1,  7,  'bank.branch.anamnagar.branch_code',       'GLB-ANA-001',                              'string'),
(1,  8,  'bank.branch.anamnagar.province',          'Bagmati Province',                         'string'),
(1,  9,  'bank.branch.anamnagar.district',          'Kathmandu',                                'string'),
(1, 10,  'bank.branch.anamnagar.city',              'Kathmandu',                                'string'),
(1, 11,  'bank.branch.anamnagar.atm_available',     'Yes',                                      'string'),
(1, 12,  'bank.branch.anamnagar.parking_available', 'Yes',                                      'string'),

-- Instance: baneshwor
(1,  1,  'bank.branch.baneshwor.address',           'New Baneshwor, Kathmandu, Bagmati Province', 'string'),
(1,  2,  'bank.branch.baneshwor.phone',             '01-4780040',                               'string'),
(1,  3,  'bank.branch.baneshwor.email',             'baneshwor@globalbank.com.np',              'string'),
(1,  4,  'bank.branch.baneshwor.website',           'www.globalbank.com.np',                    'string'),
(1,  5,  'bank.branch.baneshwor.manager',           'Sunita Karmacharya',                       'string'),
(1,  6,  'bank.branch.baneshwor.opening_hours',     'Sunday–Friday 10:00 AM – 5:00 PM',        'string'),
(1,  7,  'bank.branch.baneshwor.branch_code',       'GLB-BAN-002',                              'string'),
(1,  8,  'bank.branch.baneshwor.province',          'Bagmati Province',                         'string'),
(1,  9,  'bank.branch.baneshwor.district',          'Kathmandu',                                'string'),
(1, 10,  'bank.branch.baneshwor.city',              'Kathmandu',                                'string'),
(1, 11,  'bank.branch.baneshwor.atm_available',     'Yes',                                      'string'),
(1, 12,  'bank.branch.baneshwor.parking_available', 'No',                                       'string'),

-- Instance: kalanki
(1,  1,  'bank.branch.kalanki.address',             'Kalanki Chowk, Kathmandu, Bagmati Province', 'string'),
(1,  2,  'bank.branch.kalanki.phone',               '01-5319020',                               'string'),
(1,  3,  'bank.branch.kalanki.email',               'kalanki@globalbank.com.np',                'string'),
(1,  4,  'bank.branch.kalanki.website',             'www.globalbank.com.np',                    'string'),
(1,  5,  'bank.branch.kalanki.manager',             'Bikash Pandey',                            'string'),
(1,  6,  'bank.branch.kalanki.opening_hours',       'Sunday–Friday 10:00 AM – 5:00 PM',        'string'),
(1,  7,  'bank.branch.kalanki.branch_code',         'GLB-KAL-003',                              'string'),
(1,  8,  'bank.branch.kalanki.province',            'Bagmati Province',                         'string'),
(1,  9,  'bank.branch.kalanki.district',            'Kathmandu',                                'string'),
(1, 10,  'bank.branch.kalanki.city',                'Kathmandu',                                'string'),
(1, 11,  'bank.branch.kalanki.atm_available',       'Yes',                                      'string'),
(1, 12,  'bank.branch.kalanki.parking_available',   'Yes',                                      'string'),

-- Instance: pokhara
(1,  1,  'bank.branch.pokhara.address',             'Lakeside, Pokhara, Gandaki Province',      'string'),
(1,  2,  'bank.branch.pokhara.phone',               '061-530040',                               'string'),
(1,  3,  'bank.branch.pokhara.email',               'pokhara@globalbank.com.np',                'string'),
(1,  4,  'bank.branch.pokhara.website',             'www.globalbank.com.np',                    'string'),
(1,  5,  'bank.branch.pokhara.manager',             'Anita Gurung',                             'string'),
(1,  6,  'bank.branch.pokhara.opening_hours',       'Sunday–Friday 10:00 AM – 5:00 PM',        'string'),
(1,  7,  'bank.branch.pokhara.branch_code',         'GLB-PKR-004',                              'string'),
(1,  8,  'bank.branch.pokhara.province',            'Gandaki Province',                         'string'),
(1,  9,  'bank.branch.pokhara.district',            'Kaski',                                    'string'),
(1, 10,  'bank.branch.pokhara.city',                'Pokhara',                                  'string'),
(1, 11,  'bank.branch.pokhara.atm_available',       'Yes',                                      'string'),
(1, 12,  'bank.branch.pokhara.parking_available',   'Yes',                                      'string'),


-- ── Category: loan (entity_id=2) ─────────────────────────────────────
-- Instance: home_loan
(2, 13,  'bank.loan.home_loan.interest_rate',        '8.5',                                      'numeric'),
(2, 14,  'bank.loan.home_loan.minimum_loan_amount',  '500000',                                   'numeric'),
(2, 15,  'bank.loan.home_loan.maximum_loan_amount',  '50000000',                                 'numeric'),
(2, 16,  'bank.loan.home_loan.minimum_tenure',       '1',                                        'numeric'),
(2, 17,  'bank.loan.home_loan.maximum_tenure',       '25',                                       'numeric'),
(2, 18,  'bank.loan.home_loan.processing_fee',       '0.5',                                      'numeric'),
(2, 19,  'bank.loan.home_loan.collateral',           'Property or Land',                         'string'),
(2, 20,  'bank.loan.home_loan.eligibility',          'Nepali citizen, minimum age 21, stable income', 'string'),
(2, 21,  'bank.loan.home_loan.required_documents',   'Citizenship, Land certificate, Income proof, Property valuation', 'string'),
(2, 22,  'bank.loan.home_loan.loan_type',            'Secured',                                  'string'),

-- Instance: education_loan
(2, 13,  'bank.loan.education_loan.interest_rate',       '9.0',                                      'numeric'),
(2, 14,  'bank.loan.education_loan.minimum_loan_amount', '100000',                                   'numeric'),
(2, 15,  'bank.loan.education_loan.maximum_loan_amount', '5000000',                                  'numeric'),
(2, 16,  'bank.loan.education_loan.minimum_tenure',      '1',                                        'numeric'),
(2, 17,  'bank.loan.education_loan.maximum_tenure',      '7',                                        'numeric'),
(2, 18,  'bank.loan.education_loan.processing_fee',      '0.75',                                     'numeric'),
(2, 19,  'bank.loan.education_loan.collateral',          'Property or Guarantor',                    'string'),
(2, 20,  'bank.loan.education_loan.eligibility',         'Admitted to recognized institution, age 16–40', 'string'),
(2, 21,  'bank.loan.education_loan.required_documents',  'Citizenship, Admission letter, Fee structure, Guarantor documents', 'string'),
(2, 22,  'bank.loan.education_loan.loan_type',           'Secured',                                  'string'),

-- Instance: personal_loan
(2, 13,  'bank.loan.personal_loan.interest_rate',        '12.5',                                     'numeric'),
(2, 14,  'bank.loan.personal_loan.minimum_loan_amount',  '50000',                                    'numeric'),
(2, 15,  'bank.loan.personal_loan.maximum_loan_amount',  '1000000',                                  'numeric'),
(2, 16,  'bank.loan.personal_loan.minimum_tenure',       '1',                                        'numeric'),
(2, 17,  'bank.loan.personal_loan.maximum_tenure',       '5',                                        'numeric'),
(2, 18,  'bank.loan.personal_loan.processing_fee',       '1.0',                                      'numeric'),
(2, 19,  'bank.loan.personal_loan.collateral',           'None',                                     'string'),
(2, 20,  'bank.loan.personal_loan.eligibility',          'Nepali citizen, age 21–60, minimum income NPR 25000/month', 'string'),
(2, 21,  'bank.loan.personal_loan.required_documents',   'Citizenship, Salary slip, Bank statement, Employment letter', 'string'),
(2, 22,  'bank.loan.personal_loan.loan_type',            'Unsecured',                                'string'),

-- Instance: auto_loan
(2, 13,  'bank.loan.auto_loan.interest_rate',            '11.0',                                     'numeric'),
(2, 14,  'bank.loan.auto_loan.minimum_loan_amount',      '200000',                                   'numeric'),
(2, 15,  'bank.loan.auto_loan.maximum_loan_amount',      '5000000',                                  'numeric'),
(2, 16,  'bank.loan.auto_loan.minimum_tenure',           '1',                                        'numeric'),
(2, 17,  'bank.loan.auto_loan.maximum_tenure',           '7',                                        'numeric'),
(2, 18,  'bank.loan.auto_loan.processing_fee',           '0.75',                                     'numeric'),
(2, 19,  'bank.loan.auto_loan.collateral',               'Vehicle',                                  'string'),
(2, 20,  'bank.loan.auto_loan.eligibility',              'Nepali citizen, age 21–60, stable income', 'string'),
(2, 21,  'bank.loan.auto_loan.required_documents',       'Citizenship, Vehicle quotation, Income proof, Insurance', 'string'),
(2, 22,  'bank.loan.auto_loan.loan_type',                'Secured',                                  'string'),


-- ── Category: card (entity_id=3) ─────────────────────────────────────
-- Instance: debit_card
(3, 28,  'bank.card.debit_card.annual_fee',              '250',                                      'numeric'),
(3, 29,  'bank.card.debit_card.joining_fee',             '500',                                      'numeric'),
(3, 30,  'bank.card.debit_card.cashback',                '0.5',                                      'numeric'),
(3, 31,  'bank.card.debit_card.reward_points',           'Not applicable',                           'string'),
(3, 32,  'bank.card.debit_card.replacement_fee',         '300',                                      'numeric'),
(3, 33,  'bank.card.debit_card.pin_generation',          'Via ATM or mobile banking',                'string'),
(3, 34,  'bank.card.debit_card.cash_withdrawal_limit',   '50000',                                    'numeric'),
(3, 35,  'bank.card.debit_card.transaction_limit',       '200000',                                   'numeric'),
(3, 38,  'bank.card.debit_card.supported_platforms',     'VISA, SCT, UnionPay',                      'string'),

-- Instance: credit_card
(3, 28,  'bank.card.credit_card.annual_fee',             '1500',                                     'numeric'),
(3, 29,  'bank.card.credit_card.joining_fee',            '1000',                                     'numeric'),
(3, 30,  'bank.card.credit_card.cashback',               '1.5',                                      'numeric'),
(3, 31,  'bank.card.credit_card.reward_points',          '2 points per NPR 100 spent',               'string'),
(3, 32,  'bank.card.credit_card.replacement_fee',        '500',                                      'numeric'),
(3, 33,  'bank.card.credit_card.pin_generation',         'Via SMS or internet banking',              'string'),
(3, 34,  'bank.card.credit_card.cash_withdrawal_limit',  '25000',                                    'numeric'),
(3, 35,  'bank.card.credit_card.transaction_limit',      '500000',                                   'numeric'),
(3, 38,  'bank.card.credit_card.supported_platforms',    'VISA, Mastercard',                         'string'),
(3, 20,  'bank.card.credit_card.eligibility',            'Minimum income NPR 30000/month, age 21–65','string'),


-- ── Category: atm (entity_id=4) ──────────────────────────────────────
-- Instance: atm_anamnagar
(4,  1,  'bank.atm.atm_anamnagar.address',               'Anamnagar, Kathmandu',                     'string'),
(4, 39,  'bank.atm.atm_anamnagar.availability',          '24/7',                                     'string'),
(4, 34,  'bank.atm.atm_anamnagar.cash_withdrawal_limit', '50000',                                    'numeric'),
(4, 40,  'bank.atm.atm_anamnagar.deposit_machine_available', 'Yes',                                 'string'),
(4, 41,  'bank.atm.atm_anamnagar.mini_statement',        'Yes',                                      'string'),
(4, 42,  'bank.atm.atm_anamnagar.balance_inquiry',       'Yes',                                      'string'),

-- Instance: atm_baneshwor
(4,  1,  'bank.atm.atm_baneshwor.address',               'New Baneshwor, Kathmandu',                 'string'),
(4, 39,  'bank.atm.atm_baneshwor.availability',          '24/7',                                     'string'),
(4, 34,  'bank.atm.atm_baneshwor.cash_withdrawal_limit', '50000',                                    'numeric'),
(4, 40,  'bank.atm.atm_baneshwor.deposit_machine_available', 'No',                                  'string'),
(4, 41,  'bank.atm.atm_baneshwor.mini_statement',        'Yes',                                      'string'),
(4, 42,  'bank.atm.atm_baneshwor.balance_inquiry',       'Yes',                                      'string'),


-- ── Category: account (entity_id=5) ──────────────────────────────────
-- Instance: saving_account
(5, 13,  'bank.account.saving_account.interest_rate',        '5.5',                                      'numeric'),
(5, 23,  'bank.account.saving_account.minimum_deposit',      '1000',                                     'numeric'),
(5, 24,  'bank.account.saving_account.maximum_deposit',      '500000',                                   'numeric'),
(5, 25,  'bank.account.saving_account.currency',             'NPR',                                      'string'),
(5, 26,  'bank.account.saving_account.interest_calculation', 'Quarterly',                                'string'),
(5, 20,  'bank.account.saving_account.eligibility',          'Any Nepali citizen or institution',        'string'),
(5, 21,  'bank.account.saving_account.required_documents',   'Citizenship, Passport size photo, PAN card', 'string'),

-- Instance: current_account
(5, 13,  'bank.account.current_account.interest_rate',        '0',                                        'numeric'),
(5, 23,  'bank.account.current_account.minimum_deposit',      '10000',                                    'numeric'),
(5, 25,  'bank.account.current_account.currency',             'NPR',                                      'string'),
(5, 26,  'bank.account.current_account.interest_calculation', 'No interest',                              'string'),
(5, 20,  'bank.account.current_account.eligibility',          'Business entities, firms, companies',      'string'),
(5, 21,  'bank.account.current_account.required_documents',   'Citizenship, Company registration, PAN, Board resolution', 'string'),
(5, 36,  'bank.account.current_account.service_charge',       'NPR 500 per quarter',                      'string'),

-- Instance: fixed_deposit
(5, 13,  'bank.account.fixed_deposit.interest_rate',        '10.5',                                     'numeric'),
(5, 23,  'bank.account.fixed_deposit.minimum_deposit',      '10000',                                    'numeric'),
(5, 25,  'bank.account.fixed_deposit.currency',             'NPR',                                      'string'),
(5, 26,  'bank.account.fixed_deposit.interest_calculation', 'At maturity',                              'string'),
(5, 27,  'bank.account.fixed_deposit.maturity_period',      '1 month to 5 years',                       'string'),
(5, 16,  'bank.account.fixed_deposit.minimum_tenure',       '1',                                        'numeric'),
(5, 17,  'bank.account.fixed_deposit.maximum_tenure',       '60',                                       'numeric'),

-- Instance: recurring_deposit
(5, 13,  'bank.account.recurring_deposit.interest_rate',    '9.5',                                      'numeric'),
(5, 23,  'bank.account.recurring_deposit.minimum_deposit',  '500',                                      'numeric'),
(5, 25,  'bank.account.recurring_deposit.currency',         'NPR',                                      'string'),
(5, 26,  'bank.account.recurring_deposit.interest_calculation', 'Monthly compounding',                  'string'),
(5, 16,  'bank.account.recurring_deposit.minimum_tenure',   '6',                                        'numeric'),
(5, 17,  'bank.account.recurring_deposit.maximum_tenure',   '60',                                       'numeric'),
(5, 20,  'bank.account.recurring_deposit.eligibility',      'Any Nepali citizen',                       'string'),


-- ── Category: service (entity_id=6) ──────────────────────────────────
-- Instance: mobile_banking
(6, 39,  'bank.service.mobile_banking.availability',             '24/7',                                     'string'),
(6, 38,  'bank.service.mobile_banking.supported_platforms',      'Android, iOS',                             'string'),
(6, 35,  'bank.service.mobile_banking.transaction_limit',        '200000',                                   'numeric'),
(6, 36,  'bank.service.mobile_banking.service_charge',           'Free',                                     'string'),
(6, 37,  'bank.service.mobile_banking.registration_requirement','Active bank account and registered mobile number', 'string'),

-- Instance: internet_banking
(6, 39,  'bank.service.internet_banking.availability',             '24/7',                                     'string'),
(6, 38,  'bank.service.internet_banking.supported_platforms',      'Web browser — Chrome, Firefox, Edge',     'string'),
(6, 35,  'bank.service.internet_banking.transaction_limit',        '500000',                                   'numeric'),
(6, 36,  'bank.service.internet_banking.service_charge',           'Free',                                     'string'),
(6, 37,  'bank.service.internet_banking.registration_requirement','Active account, email, and OTP verification', 'string'),

-- Instance: sms_banking
(6, 39,  'bank.service.sms_banking.availability',             '24/7',                                     'string'),
(6, 38,  'bank.service.sms_banking.supported_platforms',      'Any mobile phone',                         'string'),
(6, 35,  'bank.service.sms_banking.transaction_limit',        'Balance inquiry and mini statement only',  'string'),
(6, 36,  'bank.service.sms_banking.service_charge',           'NPR 10 per month',                         'string'),
(6, 37,  'bank.service.sms_banking.registration_requirement','Registered mobile number with the bank',    'string'),

-- Instance: qr_payment
(6, 39,  'bank.service.qr_payment.availability',             '24/7',                                     'string'),
(6, 38,  'bank.service.qr_payment.supported_platforms',      'Mobile banking app',                       'string'),
(6, 35,  'bank.service.qr_payment.transaction_limit',        '100000',                                   'numeric'),
(6, 36,  'bank.service.qr_payment.service_charge',           'Free',                                     'string'),
(6, 37,  'bank.service.qr_payment.registration_requirement','Active mobile banking account',             'string'),

-- Instance: remittance
(6, 39,  'bank.service.remittance.availability',             'Sunday–Friday 10:00 AM – 5:00 PM',        'string'),
(6, 35,  'bank.service.remittance.transaction_limit',        '2500000',                                  'numeric'),
(6, 36,  'bank.service.remittance.service_charge',           '0.1% of transfer amount, minimum NPR 100', 'string'),
(6, 38,  'bank.service.remittance.supported_platforms',      'Branch, Mobile banking, Internet banking', 'string'),
(6, 37,  'bank.service.remittance.registration_requirement','Valid ID and bank account',                 'string'),


-- ── Category: organization (entity_id=7) ─────────────────────────────
-- Instance: head_office
(7,  1,  'bank.organization.head_office.address',           'Tripureshwor, Kathmandu, Bagmati Province','string'),
(7,  2,  'bank.organization.head_office.phone',             '01-4230000',                               'string'),
(7,  3,  'bank.organization.head_office.email',             'info@globalbank.com.np',                   'string'),
(7,  4,  'bank.organization.head_office.website',           'www.globalbank.com.np',                    'string'),
(7,  5,  'bank.organization.head_office.manager',           'Prasad Adhikari',                          'string'),
(7, 48,  'bank.organization.head_office.swift_code',        'GLBKNPKA',                                 'string'),
(7, 49,  'bank.organization.head_office.established_year',  '1994',                                     'numeric'),
(7, 50,  'bank.organization.head_office.total_branches',    '42',                                       'numeric'),

-- Instance: customer_support
(7,  2,  'bank.organization.customer_support.phone',        '01-4230050',                               'string'),
(7,  3,  'bank.organization.customer_support.email',        'support@globalbank.com.np',                'string'),
(7, 43,  'bank.organization.customer_support.toll_free_number', '16600112233',                          'string'),
(7, 44,  'bank.organization.customer_support.support_hours','Sunday–Friday 8:00 AM – 8:00 PM',         'string'),
(7, 39,  'bank.organization.customer_support.availability', 'Sunday–Friday 8:00 AM – 8:00 PM',         'string'),

-- Instance: grievance_department
(7, 45,  'bank.organization.grievance_department.grievance_email', 'grievance@globalbank.com.np',       'string'),
(7, 46,  'bank.organization.grievance_department.grievance_phone', '01-4230060',                        'string'),
(7, 47,  'bank.organization.grievance_department.resolution_time', '7 working days',                    'string'),
(7, 44,  'bank.organization.grievance_department.support_hours',   'Sunday–Friday 10:00 AM – 5:00 PM', 'string'),
(7,  4,  'bank.organization.grievance_department.website',         'www.globalbank.com.np/grievance',   'string')

ON CONFLICT (entity_id, path_name) DO NOTHING;