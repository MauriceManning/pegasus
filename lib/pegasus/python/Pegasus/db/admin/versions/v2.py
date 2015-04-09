__author__ = "Rafael Ferreira da Silva"

DB_VERSION = 2

import logging

from Pegasus.db.admin.admin_loader import *
from Pegasus.db.admin.versions.base_version import *
from Pegasus.db.schema import *
from sqlalchemy.exc import *

log = logging.getLogger(__name__)

class Version(BaseVersion):
    
    def __init__(self, connection):
        super(Version, self).__init__(connection)
    

    def update(self, force=False):
        log.debug("Updating to version %s" % DB_VERSION)
        try:
            pg_ensemble.create(self.db.get_bind(), checkfirst=True)
        except (OperationalError, ProgrammingError):
            pass
        except Exception, e:
            self.db.rollback()
            raise DBAdminError(e)
        try:
            pg_ensemble_workflow.create(self.db.get_bind(), checkfirst=True)
        except (OperationalError, ProgrammingError):
            pass
        except Exception, e:
            self.db.rollback()
            raise DBAdminError(e)
        
        try:
            self.db.execute("SELECT parent_wf_id FROM workflow")
            try:
                self.db.execute("ALTER TABLE workflow ADD COLUMN db_url TEXT")
            except (OperationalError, ProgrammingError):
                pass
            except Exception, e:
                self.db.rollback()
                raise DBAdminError(e)
            return
        except Exception:
            try:
                self.db.execute("SELECT db_url FROM workflow")
            except (OperationalError, ProgrammingError):
                return
            
        data = None
        data2 = None
        try:
            data = self.db.execute("SELECT COUNT(wf_id) FROM master_workflow").first()
        except (OperationalError, ProgrammingError):
            pass
        except Exception, e:
            self.db.rollback()
            raise DBAdminError(e)
            
        try:
            data2 = self.db.execute("SELECT COUNT(wf_id) FROM master_workflowstate").first()
        except (OperationalError, ProgrammingError):
            pass
        except Exception, e:
            self.db.rollback()
            raise DBAdminError(e)
        
        if data2 is not None:
            if data2[0] > 0:
                raise DBAdminError("Table master_workflowstate already exists and is not empty.")
            else:
                self.db.execute("DROP TABLE master_workflowstate")
        if data is not None:
            if data[0] > 0:
                raise DBAdminError("Table master_workflow already exists and is not empty.")
            else:
                self.db.execute("DROP TABLE master_workflow")
               
        try:
            self.db.execute("ALTER TABLE workflow RENAME TO master_workflow")
        except (OperationalError, ProgrammingError):
            pass
        except Exception, e:
            self.db.rollback()
            raise DBAdminError(e)
        
        try:
            self.db.execute("ALTER TABLE workflowstate RENAME TO master_workflowstate")
        except (OperationalError, ProgrammingError):
            pass
        except Exception, e:
            self.db.rollback()
            raise DBAdminError(e)
                    
        self.db.commit()           

        
    def downgrade(self, force=False):
        pass