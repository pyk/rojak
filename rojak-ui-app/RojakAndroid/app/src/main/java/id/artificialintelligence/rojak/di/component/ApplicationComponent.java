package id.artificialintelligence.rojak.di.component;

import id.artificialintelligence.rojak.RojakBaseApplication;
import id.artificialintelligence.rojak.data.local.PreferencesHelper;
import id.artificialintelligence.rojak.data.remote.APIService;
import id.artificialintelligence.rojak.data.remote.UnauthorisedInterceptor;
import id.artificialintelligence.rojak.di.module.ApplicationModule;

import org.greenrobot.eventbus.EventBus;

import javax.inject.Singleton;

import dagger.Component;

@Singleton
@Component(modules = {ApplicationModule.class})
public interface ApplicationComponent {

    void inject(RojakBaseApplication baseApplication);

    void inject(UnauthorisedInterceptor unauthorisedInterceptor);

    APIService apiService();

    EventBus eventBus();

    PreferencesHelper prefsHelper();

}