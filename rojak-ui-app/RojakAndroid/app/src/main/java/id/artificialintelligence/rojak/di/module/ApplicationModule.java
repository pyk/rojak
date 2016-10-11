package id.artificialintelligence.rojak.di.module;

import id.artificialintelligence.rojak.RojakBaseApplication;
import id.artificialintelligence.rojak.data.local.PreferencesHelper;
import id.artificialintelligence.rojak.data.remote.APIService;

import org.greenrobot.eventbus.EventBus;

import javax.inject.Singleton;

import dagger.Module;
import dagger.Provides;

@Module
public class ApplicationModule {

    private final RojakBaseApplication mBaseApplication;

    public ApplicationModule(RojakBaseApplication baseApplication) {
        this.mBaseApplication = baseApplication;
    }

    @Provides
    @Singleton
    public RojakBaseApplication provideApplication() {
        return mBaseApplication;
    }

    @Provides
    @Singleton
    public APIService provideApiService() {
        return APIService.Factory.create(mBaseApplication);
    }

    @Provides
    @Singleton
    public EventBus eventBus() {
        return new EventBus();
    }

    @Provides
    @Singleton
    public PreferencesHelper prefsHelper() {
        return new PreferencesHelper(mBaseApplication);
    }

}