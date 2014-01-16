#include "CondCore/Utilities/interface/Utilities.h"

#include "CondCore/DBCommon/interface/DbConnection.h"
#include "CondCore/DBCommon/interface/DbScopedTransaction.h"
#include "CondCore/DBCommon/interface/DbTransaction.h"
#include "CondCore/DBCommon/interface/Exception.h"
#include "CondCore/MetaDataService/interface/MetaData.h"

#include "CondCore/DBCommon/interface/Time.h"
#include "CondFormats/Common/interface/TimeConversions.h"

#include "CondCore/IOVService/interface/IOVProxy.h"
#include "CondFormats/EcalObjects/interface/EcalADCToGeVConstant.h"
#include "CondFormats/DataRecord/interface/EcalADCToGeVConstantRcd.h"

#include <boost/program_options.hpp>
#include <iterator>
#include <iostream>

using namespace std;

namespace cond {
        class ADC2GeVDump : public Utilities {
                public:
                        typedef EcalADCToGeVConstant A;

                        std::string getToken(cond::DbSession & s, std::string & tag)
                        {
                                s = openDbSession("connect", true);
                                cond::MetaData metadata_svc(s);
                                cond::DbScopedTransaction transaction(s);
                                transaction.start(true);
                                std::string token = metadata_svc.getToken(tag);
                                transaction.commit();
                                std::cout << "Source iov token: " << token << "\n";
                                return token;
                        }

                        ADC2GeVDump();
                        ~ADC2GeVDump();
                        int execute();
                        void dump(const A & o, const char * filename);
        };

}

cond::ADC2GeVDump::ADC2GeVDump():Utilities("cmscond_list_iov")
{
        addConnectOption();
        addAuthenticationOptions();
        addOption<bool>("verbose","v","verbose");
        addOption<bool>("all","a","list all tags (default mode)");
        addOption<bool>("summary","s","stprint also the summary for each payload");
        addOption<cond::Time_t>("beginTime","b","begin time (first since) (optional)");
        addOption<cond::Time_t>("endTime","e","end time (last till) (optional)");
        addOption<std::string>("tag","t","list info of the specified tag");
        addOption<std::string>("output","o","output file (default: ic_dump_<tagname>_<IOV_start>_<IOV_stop>.dat)");
}

cond::ADC2GeVDump::~ADC2GeVDump(){
}


void cond::ADC2GeVDump::dump(const A & ag, const char * filename)
{
        FILE * fd = fopen(filename, "w");
        if (!fd) {
                char err[256];
                sprintf(err, "[cond::ADC2GeVDump::dump] Impossible to open file `%s' for dumping:", filename);
                perror(err);
                exit(1);
        }
        fprintf(fd, "EB= %f  EE= %f\n", ag.getEBValue(), ag.getEEValue());
}

int cond::ADC2GeVDump::execute()
{
        initializePluginManager();

        bool listAll = hasOptionValue("all");
        cond::DbSession session  = openDbSession("connect", true);
        cond::DbScopedTransaction transaction(session);
        transaction.start(true);

        if(listAll){
                cond::MetaData metadata_svc(session);
                std::vector<std::string> alltags;
                cond::DbScopedTransaction transaction(session);
                transaction.start(true);
                metadata_svc.listAllTags(alltags);
                transaction.commit();
                std::copy (alltags.begin(),
                           alltags.end(),
                           std::ostream_iterator<std::string>(std::cout,"\n")
                          );
        } else {
                std::string tag = getOptionValue<std::string>("tag");

                std::string output = hasOptionValue("output") ? getOptionValue<std::string>("output") : "ecallaserplotter.root";

                cond::MetaData metadata_svc(session);
                std::string token;
                cond::DbScopedTransaction transaction(session);
                transaction.start(true);
                transaction.commit();
                token = metadata_svc.getToken(tag);

                //std::string tokenb = metadata_svc.getToken(tagb);

                //transaction.commit();

                cond::Time_t since = std::numeric_limits<cond::Time_t>::min();
                if( hasOptionValue("beginTime" )) since = getOptionValue<cond::Time_t>("beginTime");
                cond::Time_t till = std::numeric_limits<cond::Time_t>::max();
                if( hasOptionValue("endTime" )) till = getOptionValue<cond::Time_t>("endTime");

                bool verbose = hasOptionValue("verbose");

                //cond::IOVProxy iov(session, getToken(session, tag));
                cond::IOVProxy iov(session, token);

                //since = std::max((cond::Time_t)2, cond::timeTypeSpecs[iov.timetype()].beginValue); // avoid first IOV
                //till  = std::min(till,  cond::timeTypeSpecs[iov.timetype()].endValue);

                std::cout << "since: " << since << "   till: " << till << "\n";

                iov.range(since,till);

                //std::string payloadContainer = iov.payloadContainerName();
                const std::set<std::string> payloadClasses = iov.payloadClasses();
                std::cout<<"Tag "<<tag;
                if (verbose) std::cout << "\nStamp: " << iov.iov().comment()
                        << "; time " <<  cond::time::to_boost(iov.iov().timestamp())
                                << "; revision " << iov.iov().revision();
                std::cout <<"\nTimeType " << cond::timeTypeSpecs[iov.timetype()].name
                        <<"\nPayloadClasses:\n";
                for (std::set<std::string>::const_iterator it = payloadClasses.begin(); it != payloadClasses.end(); ++it) {
                        std::cout << " --> " << *it << "\n";
                }
                std::cout
                        <<"since \t till \t payloadToken"<<std::endl;

                static const unsigned int nIOVS = std::distance(iov.begin(), iov.end());

                std::cout << "nIOVS: " << nIOVS << "\n";

                typedef unsigned int LuminosityBlockNumber_t;
                typedef unsigned int RunNumber_t;

                int cnt = 0;
                char filename[256];
                for (cond::IOVProxy::const_iterator ita = iov.begin(); ita != iov.end(); ++ita, ++cnt) {
                        std::cout << cnt << " " << ita->since() << " -> " << ita->till() << "\n";
                        boost::shared_ptr<A> pa = session.getTypedObject<A>(ita->token());
                        sprintf(filename, "dump_%s__since_%ld_till_%ld.dat", tag.c_str(), (long int)ita->since(), (long int)ita->till());
                        fprintf(stderr, "going to dump on `%s'\n", filename);
                        dump(*pa, filename);
                }
                transaction.commit();
        }
        return 0;
}


int main( int argc, char** argv )
{
        cond::ADC2GeVDump dump;
        return dump.run(argc,argv);
}
