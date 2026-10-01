"""Add October 1 property listings

Revision ID: 20261001_0001
Revises: 20260929_0006
"""
from alembic import op
import sqlalchemy as sa

revision = "20261001_0001"
down_revision = "20260929_0006"
branch_labels = None
depends_on = None

PROPERTIES = [
("Unfinished 7 Bedroom House - Zimre Park","unfinished-7-bedroom-house-zimre-park","Houses","Zimre Park, Masvingo","US$120,000 negotiable",None,7,"2,000 sqm","Unfinished 7-bedroom house in a low-density, built-up area close to GZU Campus. ZESA and water are connected.","7 bedrooms; low density; close to GZU Campus; built-up neighbourhood; ZESA connected; water connected; unfinished","Council cession, clean papers"),
("7 Room Unfinished House - Takawira","7-room-unfinished-house-takawira","Houses","Takawira, Masvingo","US$16,000",None,7,"300 sqm","7-room unfinished house at window level in Takawira, Masvingo. Developer: Unibrik.","7 rooms; at window level; Unibrik developer","Council cession"),
("8 Room House - Victoria Ranch","8-room-house-victoria-ranch","Houses","Victoria Ranch, near Jazire Creche, Masvingo","US$45,000",None,8,"250 sqm","8-room property in Victoria Ranch, near Jazire Creche, Masvingo.","8 rooms; fenced; water well","Council papers"),
("420 sqm Infill Stand - Lot A Victoria Ranch","420sqm-infill-stand-lot-a-victoria-ranch","Residential Stands","Lot A Victoria Ranch, Masvingo","US$7,000",None,None,"420 sqm","420 sqm infill stand for sale in Lot A Victoria Ranch, Masvingo.","420 sqm infill stand",None),
("7 Room House Slab - Lot A Medium","7-room-house-slab-lot-a-medium","Houses","Lot A Medium, Masvingo","US$12,000",None,7,"450 sqm","7-room house at slab level in Lot A Medium, Masvingo.","7 rooms; on slab level","Council cession"),
("4,800 sqm Stand - Westview Industrial","4800sqm-stand-westview-industrial-masvingo","Commercial & Industrial Stands","Westview Industrial Area, Masvingo","US$150,000",None,None,"4,800 sqm","Reduced-to-go 4,800 sqm stand in Westview Industrial Area, Masvingo, suitable for cluster houses or development.","4,800 sqm; suitable for cluster houses/development; reduced to go","Council papers"),
("Sports Bar for Sale - PaAminas","sports-bar-for-sale-paaminas-masvingo","Commercial Buildings","PaAminas, Masvingo","US$90,000",None,None,"300 sqm","Sports bar for sale in a prime business location at PaAminas, Masvingo. Ready to operate.","Sports bar; prime business location; ready to operate",None),
("8 Room House - KMP","8-room-house-kmp-masvingo","Houses","KMP, Masvingo","US$46,000",None,8,"350 sqm","Finished 8-room house in a built-up area of KMP, Masvingo, ready for occupation.","8 rooms; finished house; solar geyser; satellite dish; durawall; metal gate; walled and secure","Council cession, clean papers; verification before payment"),
("588 sqm Stand - Zexcom","588sqm-stand-zexcom-masvingo","Residential Stands","Zexcom, Masvingo","US$12,000",None,None,"588 sqm","588 sqm residential stand in a built-up area of Zexcom, Masvingo, ready to build.","Built-up area; ready to build","Council cession; verification before payment"),
("240 sqm Lot A Commercial Stand","240sqm-lot-a-commercial-stand-masvingo","Commercial Stands","Lot A Commercial, Masvingo","US$8,000",None,None,"240 sqm","240 sqm commercial stand in Masvingo Commercial.","ZESA poles available; ready to build","Council cession"),
("2 Room House - Phase Mufamba","2-room-house-phase-mufamba-vic-range","Houses","Phase Mufamba, Victoria Range","US$13,000",None,2,None,"2-room property for sale in Phase Mufamba, Victoria Range.","2 rooms",None),
("5 Room Semi-Detached House - Sisk","5-room-semi-detached-house-sisk-masvingo","Houses","Sisk, Masvingo","US$35,000",None,5,"250 sqm","5-room semi-detached house in Sisk, Masvingo.","5 rooms; semi-detached; ZESA; sewer; tarred roads; water","Council papers"),
("9 Room House - Pambudzi","9-room-house-pambudzi-masvingo","Houses","Pambudzi, Masvingo","US$65,000",None,9,"525 sqm","9-room house in a built-up neighbourhood in Pambudzi, Masvingo, ready to move in.","9 rooms; built-up neighbourhood; ZESA connected; ready to move in","Council cession, clean papers, admin fee paid"),
("Madokero Warehouse for Sale","madokero-warehouse-for-sale","Commercial Buildings","Madokero, Harare","US$1,000,000",None,None,"5,500 sqm","Warehouse property for sale seated on 5,500 sqm of land. The property includes a 2,000 sqm warehouse floor and 440 sqm of offices. Ready for use.","2,000 sqm warehouse floor; 440 sqm offices; high-clearance steel structure; ready for use",None),
]

def upgrade():
    conn = op.get_bind()
    stmt = sa.text("""
        INSERT INTO properties
        (title, slug, property_type, location, price, bedrooms, rooms, stand_size,
         description, features, paperwork_status, status, featured)
        SELECT
          :title, :slug, :property_type, :location, :price, :bedrooms, :rooms,
          :stand_size, :description, :features, :paperwork_status,
          'available', FALSE
        WHERE NOT EXISTS (SELECT 1 FROM properties WHERE slug = :slug)
    """)
    for row in PROPERTIES:
        conn.execute(stmt, dict(zip(
            ["title","slug","property_type","location","price","bedrooms","rooms",
             "stand_size","description","features","paperwork_status"], row
        )))

def downgrade():
    conn = op.get_bind()
    conn.execute(
        sa.text("DELETE FROM properties WHERE slug = ANY(:slugs)"),
        {"slugs": [row[1] for row in PROPERTIES]},
    )
