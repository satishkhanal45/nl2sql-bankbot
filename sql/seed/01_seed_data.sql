-- ============================================================
-- SEED DATA: entity
-- ============================================================


INSERT INTO entity (entity_name, fact) VALUES
    -- Branches
    ('bank', 'branch_anamnagar'),
    ('bank', 'branch_baneshwor'),
    ('bank', 'branch_kalanki'),
    ('bank', 'branch_pokhara'),
    -- Products
    ('bank', 'home_loan'),
    ('bank', 'education_loan'),
    ('bank', 'personal_loan'),
    ('bank', 'auto_loan'),
    ('bank', 'saving_account'),
    ('bank', 'current_account'),
    ('bank', 'fixed_deposit'),
    ('bank', 'recurring_deposit'),
    -- Cards
    ('bank', 'debit_card'),
    ('bank', 'credit_card'),
    -- Services
    ('bank', 'mobile_banking'),
    ('bank', 'internet_banking'),
    ('bank', 'sms_banking'),
    ('bank', 'qr_payment'),
    ('bank', 'remittance'),
    -- ATM
    ('bank', 'atm_anamnagar'),
    ('bank', 'atm_baneshwor'),
    -- Organization
    ('bank', 'head_office'),
    ('bank', 'customer_support'),
    ('bank', 'grievance_department')
ON CONFLICT (entity_name, fact) DO NOTHING;


-- ============================================================
-- SEED DATA: attribute
-- ============================================================
INSERT INTO attribute (label) VALUES
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
    ('minimum_deposit'),
    ('maximum_deposit'),
    ('currency'),
    ('interest_calculation'),
    ('maturity_period'),
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
    ('availability'),
    ('deposit_machine_available'),
    ('mini_statement'),
    ('balance_inquiry'),
    ('toll_free_number'),
    ('support_hours'),
    ('grievance_email'),
    ('grievance_phone'),
    ('resolution_time'),
    ('swift_code'),
    ('established_year'),
    ('total_branches')
ON CONFLICT (label) DO NOTHING;



INSERT INTO entity_value (entity_id, attribute_id, path_name, value, type) VALUES

-- ── branch_anamnagar (entity_id=1) ────────────────────────
(1,  1,  'bank.branch_anamnagar.address',          'Anamnagar, Kathmandu, Bagmati Province',   'string'),
(1,  2,  'bank.branch_anamnagar.phone',             '01-4102030',                               'string'),
(1,  3,  'bank.branch_anamnagar.email',             'anamnagar@globalbank.com.np',              'string'),
(1,  4,  'bank.branch_anamnagar.website',           'www.globalbank.com.np',                    'string'),
(1,  5,  'bank.branch_anamnagar.manager',           'Ramesh Shrestha',                          'string'),
(1,  6,  'bank.branch_anamnagar.opening_hours',     'Sunday–Friday 10:00 AM – 5:00 PM',        'string'),
(1,  7,  'bank.branch_anamnagar.branch_code',       'GLB-ANA-001',                              'string'),
(1,  8,  'bank.branch_anamnagar.province',          'Bagmati Province',                         'string'),
(1,  9,  'bank.branch_anamnagar.district',          'Kathmandu',                                'string'),
(1, 10,  'bank.branch_anamnagar.city',              'Kathmandu',                                'string'),
(1, 11,  'bank.branch_anamnagar.atm_available',     'Yes',                                      'string'),
(1, 12,  'bank.branch_anamnagar.parking_available', 'Yes',                                      'string'),

-- ── branch_baneshwor (entity_id=2) ───────────────────────
(2,  1,  'bank.branch_baneshwor.address',           'New Baneshwor, Kathmandu, Bagmati Province', 'string'),
(2,  2,  'bank.branch_baneshwor.phone',             '01-4780040',                               'string'),
(2,  3,  'bank.branch_baneshwor.email',             'baneshwor@globalbank.com.np',              'string'),
(2,  4,  'bank.branch_baneshwor.website',           'www.globalbank.com.np',                    'string'),
(2,  5,  'bank.branch_baneshwor.manager',           'Sunita Karmacharya',                       'string'),
(2,  6,  'bank.branch_baneshwor.opening_hours',     'Sunday–Friday 10:00 AM – 5:00 PM',        'string'),
(2,  7,  'bank.branch_baneshwor.branch_code',       'GLB-BAN-002',                              'string'),
(2,  8,  'bank.branch_baneshwor.province',          'Bagmati Province',                         'string'),
(2,  9,  'bank.branch_baneshwor.district',          'Kathmandu',                                'string'),
(2, 10,  'bank.branch_baneshwor.city',              'Kathmandu',                                'string'),
(2, 11,  'bank.branch_baneshwor.atm_available',     'Yes',                                      'string'),
(2, 12,  'bank.branch_baneshwor.parking_available', 'No',                                       'string'),

-- ── branch_kalanki (entity_id=3) ─────────────────────────
(3,  1,  'bank.branch_kalanki.address',             'Kalanki Chowk, Kathmandu, Bagmati Province', 'string'),
(3,  2,  'bank.branch_kalanki.phone',               '01-5319020',                               'string'),
(3,  3,  'bank.branch_kalanki.email',               'kalanki@globalbank.com.np',                'string'),
(3,  4,  'bank.branch_kalanki.website',             'www.globalbank.com.np',                    'string'),
(3,  5,  'bank.branch_kalanki.manager',             'Bikash Pandey',                            'string'),
(3,  6,  'bank.branch_kalanki.opening_hours',       'Sunday–Friday 10:00 AM – 5:00 PM',        'string'),
(3,  7,  'bank.branch_kalanki.branch_code',         'GLB-KAL-003',                              'string'),
(3,  8,  'bank.branch_kalanki.province',            'Bagmati Province',                         'string'),
(3,  9,  'bank.branch_kalanki.district',            'Kathmandu',                                'string'),
(3, 10,  'bank.branch_kalanki.city',                'Kathmandu',                                'string'),
(3, 11,  'bank.branch_kalanki.atm_available',       'Yes',                                      'string'),
(3, 12,  'bank.branch_kalanki.parking_available',   'Yes',                                      'string'),

-- ── branch_pokhara (entity_id=4) ─────────────────────────
(4,  1,  'bank.branch_pokhara.address',             'Lakeside, Pokhara, Gandaki Province',      'string'),
(4,  2,  'bank.branch_pokhara.phone',               '061-530040',                               'string'),
(4,  3,  'bank.branch_pokhara.email',               'pokhara@globalbank.com.np',                'string'),
(4,  4,  'bank.branch_pokhara.website',             'www.globalbank.com.np',                    'string'),
(4,  5,  'bank.branch_pokhara.manager',             'Anita Gurung',                             'string'),
(4,  6,  'bank.branch_pokhara.opening_hours',       'Sunday–Friday 10:00 AM – 5:00 PM',        'string'),
(4,  7,  'bank.branch_pokhara.branch_code',         'GLB-PKR-004',                              'string'),
(4,  8,  'bank.branch_pokhara.province',            'Gandaki Province',                         'string'),
(4,  9,  'bank.branch_pokhara.district',            'Kaski',                                    'string'),
(4, 10,  'bank.branch_pokhara.city',                'Pokhara',                                  'string'),
(4, 11,  'bank.branch_pokhara.atm_available',       'Yes',                                      'string'),
(4, 12,  'bank.branch_pokhara.parking_available',   'Yes',                                      'string'),

-- ── home_loan (entity_id=5) ───────────────────────────────
(5, 13,  'bank.home_loan.interest_rate',            '8.5',                                      'numeric'),
(5, 14,  'bank.home_loan.minimum_loan_amount',      '500000',                                   'numeric'),
(5, 15,  'bank.home_loan.maximum_loan_amount',      '50000000',                                 'numeric'),
(5, 16,  'bank.home_loan.minimum_tenure',           '1',                                        'numeric'),
(5, 17,  'bank.home_loan.maximum_tenure',           '25',                                       'numeric'),
(5, 18,  'bank.home_loan.processing_fee',           '0.5',                                      'numeric'),
(5, 19,  'bank.home_loan.collateral',               'Property or Land',                         'string'),
(5, 20,  'bank.home_loan.eligibility',              'Nepali citizen, minimum age 21, stable income', 'string'),
(5, 21,  'bank.home_loan.required_documents',       'Citizenship, Land certificate, Income proof, Property valuation', 'string'),
(5, 22,  'bank.home_loan.loan_type',                'Secured',                                  'string'),

-- ── education_loan (entity_id=6) ─────────────────────────
(6, 13,  'bank.education_loan.interest_rate',       '9.0',                                      'numeric'),
(6, 14,  'bank.education_loan.minimum_loan_amount', '100000',                                   'numeric'),
(6, 15,  'bank.education_loan.maximum_loan_amount', '5000000',                                  'numeric'),
(6, 16,  'bank.education_loan.minimum_tenure',      '1',                                        'numeric'),
(6, 17,  'bank.education_loan.maximum_tenure',      '7',                                        'numeric'),
(6, 18,  'bank.education_loan.processing_fee',      '0.75',                                     'numeric'),
(6, 19,  'bank.education_loan.collateral',          'Property or Guarantor',                    'string'),
(6, 20,  'bank.education_loan.eligibility',         'Admitted to recognized institution, age 16–40', 'string'),
(6, 21,  'bank.education_loan.required_documents',  'Citizenship, Admission letter, Fee structure, Guarantor documents', 'string'),
(6, 22,  'bank.education_loan.loan_type',           'Secured',                                  'string'),

-- ── personal_loan (entity_id=7) ──────────────────────────
(7, 13,  'bank.personal_loan.interest_rate',        '12.5',                                     'numeric'),
(7, 14,  'bank.personal_loan.minimum_loan_amount',  '50000',                                    'numeric'),
(7, 15,  'bank.personal_loan.maximum_loan_amount',  '1000000',                                  'numeric'),
(7, 16,  'bank.personal_loan.minimum_tenure',       '1',                                        'numeric'),
(7, 17,  'bank.personal_loan.maximum_tenure',       '5',                                        'numeric'),
(7, 18,  'bank.personal_loan.processing_fee',       '1.0',                                      'numeric'),
(7, 19,  'bank.personal_loan.collateral',           'None',                                     'string'),
(7, 20,  'bank.personal_loan.eligibility',          'Nepali citizen, age 21–60, minimum income NPR 25000/month', 'string'),
(7, 21,  'bank.personal_loan.required_documents',   'Citizenship, Salary slip, Bank statement, Employment letter', 'string'),
(7, 22,  'bank.personal_loan.loan_type',            'Unsecured',                                'string'),

-- ── auto_loan (entity_id=8) ───────────────────────────────
(8, 13,  'bank.auto_loan.interest_rate',            '11.0',                                     'numeric'),
(8, 14,  'bank.auto_loan.minimum_loan_amount',      '200000',                                   'numeric'),
(8, 15,  'bank.auto_loan.maximum_loan_amount',      '5000000',                                  'numeric'),
(8, 16,  'bank.auto_loan.minimum_tenure',           '1',                                        'numeric'),
(8, 17,  'bank.auto_loan.maximum_tenure',           '7',                                        'numeric'),
(8, 18,  'bank.auto_loan.processing_fee',           '0.75',                                     'numeric'),
(8, 19,  'bank.auto_loan.collateral',               'Vehicle',                                  'string'),
(8, 20,  'bank.auto_loan.eligibility',              'Nepali citizen, age 21–60, stable income', 'string'),
(8, 21,  'bank.auto_loan.required_documents',       'Citizenship, Vehicle quotation, Income proof, Insurance', 'string'),
(8, 22,  'bank.auto_loan.loan_type',                'Secured',                                  'string'),

-- ── saving_account (entity_id=9) ─────────────────────────
(9, 13,  'bank.saving_account.interest_rate',       '5.5',                                      'numeric'),
(9, 23,  'bank.saving_account.minimum_deposit',     '1000',                                     'numeric'),
(9, 24,  'bank.saving_account.maximum_deposit',     '500000',                                   'numeric'),
(9, 25,  'bank.saving_account.currency',            'NPR',                                      'string'),
(9, 26,  'bank.saving_account.interest_calculation','Quarterly',                                'string'),
(9, 20,  'bank.saving_account.eligibility',         'Any Nepali citizen or institution',        'string'),
(9, 21,  'bank.saving_account.required_documents',  'Citizenship, Passport size photo, PAN card', 'string'),

-- ── current_account (entity_id=10) ───────────────────────
(10, 13, 'bank.current_account.interest_rate',      '0',                                        'numeric'),
(10, 23, 'bank.current_account.minimum_deposit',    '10000',                                    'numeric'),
(10, 25, 'bank.current_account.currency',           'NPR',                                      'string'),
(10, 26, 'bank.current_account.interest_calculation','No interest',                             'string'),
(10, 20, 'bank.current_account.eligibility',        'Business entities, firms, companies',      'string'),
(10, 21, 'bank.current_account.required_documents', 'Citizenship, Company registration, PAN, Board resolution', 'string'),
(10, 36, 'bank.current_account.service_charge',     'NPR 500 per quarter',                      'string'),

-- ── fixed_deposit (entity_id=11) ─────────────────────────
(11, 13, 'bank.fixed_deposit.interest_rate',        '10.5',                                     'numeric'),
(11, 23, 'bank.fixed_deposit.minimum_deposit',      '10000',                                    'numeric'),
(11, 25, 'bank.fixed_deposit.currency',             'NPR',                                      'string'),
(11, 26, 'bank.fixed_deposit.interest_calculation', 'At maturity',                              'string'),
(11, 27, 'bank.fixed_deposit.maturity_period',      '1 month to 5 years',                       'string'),
(11, 16, 'bank.fixed_deposit.minimum_tenure',       '1',                                        'numeric'),
(11, 17, 'bank.fixed_deposit.maximum_tenure',       '60',                                       'numeric'),

-- ── recurring_deposit (entity_id=12) ─────────────────────
(12, 13, 'bank.recurring_deposit.interest_rate',    '9.5',                                      'numeric'),
(12, 23, 'bank.recurring_deposit.minimum_deposit',  '500',                                      'numeric'),
(12, 25, 'bank.recurring_deposit.currency',         'NPR',                                      'string'),
(12, 26, 'bank.recurring_deposit.interest_calculation', 'Monthly compounding',                  'string'),
(12, 16, 'bank.recurring_deposit.minimum_tenure',   '6',                                        'numeric'),
(12, 17, 'bank.recurring_deposit.maximum_tenure',   '60',                                       'numeric'),
(12, 20, 'bank.recurring_deposit.eligibility',      'Any Nepali citizen',                       'string'),

-- ── debit_card (entity_id=13) ─────────────────────────────
(13, 28, 'bank.debit_card.annual_fee',              '250',                                      'numeric'),
(13, 29, 'bank.debit_card.joining_fee',             '500',                                      'numeric'),
(13, 30, 'bank.debit_card.cashback',                '0.5',                                      'numeric'),
(13, 31, 'bank.debit_card.reward_points',           'Not applicable',                           'string'),
(13, 32, 'bank.debit_card.replacement_fee',         '300',                                      'numeric'),
(13, 33, 'bank.debit_card.pin_generation',          'Via ATM or mobile banking',                'string'),
(13, 34, 'bank.debit_card.cash_withdrawal_limit',   '50000',                                    'numeric'),
(13, 35, 'bank.debit_card.transaction_limit',       '200000',                                   'numeric'),
(13, 38, 'bank.debit_card.supported_platforms',     'VISA, SCT, UnionPay',                      'string'),

-- ── credit_card (entity_id=14) ────────────────────────────
(14, 28, 'bank.credit_card.annual_fee',             '1500',                                     'numeric'),
(14, 29, 'bank.credit_card.joining_fee',            '1000',                                     'numeric'),
(14, 30, 'bank.credit_card.cashback',               '1.5',                                      'numeric'),
(14, 31, 'bank.credit_card.reward_points',          '2 points per NPR 100 spent',               'string'),
(14, 32, 'bank.credit_card.replacement_fee',        '500',                                      'numeric'),
(14, 33, 'bank.credit_card.pin_generation',         'Via SMS or internet banking',              'string'),
(14, 34, 'bank.credit_card.cash_withdrawal_limit',  '25000',                                    'numeric'),
(14, 35, 'bank.credit_card.transaction_limit',      '500000',                                   'numeric'),
(14, 38, 'bank.credit_card.supported_platforms',    'VISA, Mastercard',                         'string'),
(14, 20, 'bank.credit_card.eligibility',            'Minimum income NPR 30000/month, age 21–65','string'),

-- ── mobile_banking (entity_id=15) ─────────────────────────
(15, 39, 'bank.mobile_banking.availability',        '24/7',                                     'string'),
(15, 38, 'bank.mobile_banking.supported_platforms', 'Android, iOS',                             'string'),
(15, 35, 'bank.mobile_banking.transaction_limit',   '200000',                                   'numeric'),
(15, 36, 'bank.mobile_banking.service_charge',      'Free',                                     'string'),
(15, 37, 'bank.mobile_banking.registration_requirement', 'Active bank account and registered mobile number', 'string'),

-- ── internet_banking (entity_id=16) ──────────────────────
(16, 39, 'bank.internet_banking.availability',      '24/7',                                     'string'),
(16, 38, 'bank.internet_banking.supported_platforms','Web browser — Chrome, Firefox, Edge',     'string'),
(16, 35, 'bank.internet_banking.transaction_limit', '500000',                                   'numeric'),
(16, 36, 'bank.internet_banking.service_charge',    'Free',                                     'string'),
(16, 37, 'bank.internet_banking.registration_requirement', 'Active account, email, and OTP verification', 'string'),

-- ── sms_banking (entity_id=17) ────────────────────────────
(17, 39, 'bank.sms_banking.availability',           '24/7',                                     'string'),
(17, 38, 'bank.sms_banking.supported_platforms',    'Any mobile phone',                         'string'),
(17, 35, 'bank.sms_banking.transaction_limit',      'Balance inquiry and mini statement only',  'string'),
(17, 36, 'bank.sms_banking.service_charge',         'NPR 10 per month',                         'string'),
(17, 37, 'bank.sms_banking.registration_requirement','Registered mobile number with the bank',  'string'),

-- ── qr_payment (entity_id=18) ─────────────────────────────
(18, 39, 'bank.qr_payment.availability',            '24/7',                                     'string'),
(18, 38, 'bank.qr_payment.supported_platforms',     'Mobile banking app',                       'string'),
(18, 35, 'bank.qr_payment.transaction_limit',       '100000',                                   'numeric'),
(18, 36, 'bank.qr_payment.service_charge',          'Free',                                     'string'),
(18, 37, 'bank.qr_payment.registration_requirement','Active mobile banking account',            'string'),

-- ── remittance (entity_id=19) ─────────────────────────────
(19, 39, 'bank.remittance.availability',            'Sunday–Friday 10:00 AM – 5:00 PM',        'string'),
(19, 35, 'bank.remittance.transaction_limit',       '2500000',                                  'numeric'),
(19, 36, 'bank.remittance.service_charge',          '0.1% of transfer amount, minimum NPR 100', 'string'),
(19, 38, 'bank.remittance.supported_platforms',     'Branch, Mobile banking, Internet banking', 'string'),
(19, 37, 'bank.remittance.registration_requirement','Valid ID and bank account',                'string'),

-- ── atm_anamnagar (entity_id=20) ─────────────────────────
(20,  1, 'bank.atm_anamnagar.address',              'Anamnagar, Kathmandu',                     'string'),
(20, 39, 'bank.atm_anamnagar.availability',         '24/7',                                     'string'),
(20, 34, 'bank.atm_anamnagar.cash_withdrawal_limit','50000',                                    'numeric'),
(20, 40, 'bank.atm_anamnagar.deposit_machine_available', 'Yes',                                 'string'),
(20, 41, 'bank.atm_anamnagar.mini_statement',       'Yes',                                      'string'),
(20, 42, 'bank.atm_anamnagar.balance_inquiry',      'Yes',                                      'string'),

-- ── atm_baneshwor (entity_id=21) ─────────────────────────
(21,  1, 'bank.atm_baneshwor.address',              'New Baneshwor, Kathmandu',                 'string'),
(21, 39, 'bank.atm_baneshwor.availability',         '24/7',                                     'string'),
(21, 34, 'bank.atm_baneshwor.cash_withdrawal_limit','50000',                                    'numeric'),
(21, 40, 'bank.atm_baneshwor.deposit_machine_available', 'No',                                  'string'),
(21, 41, 'bank.atm_baneshwor.mini_statement',       'Yes',                                      'string'),
(21, 42, 'bank.atm_baneshwor.balance_inquiry',      'Yes',                                      'string'),

-- ── head_office (entity_id=22) ────────────────────────────
(22,  1, 'bank.head_office.address',                'Tripureshwor, Kathmandu, Bagmati Province','string'),
(22,  2, 'bank.head_office.phone',                  '01-4230000',                               'string'),
(22,  3, 'bank.head_office.email',                  'info@globalbank.com.np',                   'string'),
(22,  4, 'bank.head_office.website',                'www.globalbank.com.np',                    'string'),
(22,  5, 'bank.head_office.manager',                'Prasad Adhikari',                          'string'),
(22, 48, 'bank.head_office.swift_code',             'GLBKNPKA',                                 'string'),
(22, 49, 'bank.head_office.established_year',       '1994',                                     'numeric'),
(22, 50, 'bank.head_office.total_branches',         '42',                                       'numeric'),

-- ── customer_support (entity_id=23) ──────────────────────
(23,  2, 'bank.customer_support.phone',             '01-4230050',                               'string'),
(23,  3, 'bank.customer_support.email',             'support@globalbank.com.np',                'string'),
(23, 43, 'bank.customer_support.toll_free_number',  '16600112233',                              'string'),
(23, 44, 'bank.customer_support.support_hours',     'Sunday–Friday 8:00 AM – 8:00 PM',         'string'),
(23, 39, 'bank.customer_support.availability',      'Sunday–Friday 8:00 AM – 8:00 PM',         'string'),

-- ── grievance_department (entity_id=24) ──────────────────
(24, 45, 'bank.grievance_department.grievance_email',   'grievance@globalbank.com.np',          'string'),
(24, 46, 'bank.grievance_department.grievance_phone',   '01-4230060',                           'string'),
(24, 47, 'bank.grievance_department.resolution_time',   '7 working days',                       'string'),
(24, 44, 'bank.grievance_department.support_hours',     'Sunday–Friday 10:00 AM – 5:00 PM',    'string'),
(24,  4, 'bank.grievance_department.website',           'www.globalbank.com.np/grievance',      'string')

ON CONFLICT (entity_id, attribute_id) DO NOTHING;